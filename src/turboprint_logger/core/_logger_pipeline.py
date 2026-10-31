from __future__ import annotations

import sys
from collections.abc import Callable
from contextlib import suppress
from typing import TYPE_CHECKING, Any, cast

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.managers import (
    ContextManager,
    FiltersManager,
    HandlersManager,
    LevelManager,
    MetricsManager,
    ProcessorsManager,
    StatusManager,
    TagsManager,
)
from turboprint_logger.utils.normalizers import (
    normalize_context_key,
    normalize_level_name,
)

if TYPE_CHECKING:
    from turboprint_logger.core.container import Container
    from turboprint_logger.core.logger import Logger

__all__ = ("_LoggerPipeline",)


class _LoggerPipeline:
    _container: Container
    context: ContextManager
    filters: FiltersManager
    handlers: HandlersManager
    level: LevelManager
    metrics: MetricsManager
    parent: Logger
    processors: ProcessorsManager
    propagate: bool
    status: StatusManager
    tags: TagsManager

    def _merge_tags(self, tags: list[str] | None = None) -> set[str]:
        merged: set[str] = set()
        merged.update(self._container.globals.tags.get())
        merged.update(self.tags.get())
        merged.update(tags or [])
        return merged

    def _merge_context(self, extra: dict[str, Any]) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        merged.update(self._container.globals.context.get())
        merged.update(self.context.get())

        processed: dict[str, Any] = {}
        for key, value in extra.items():
            if hasattr(value, "__log__") and callable(value.__log__):
                try:
                    extracted = value.__log__()
                except Exception as exc:  # noqa: BLE001
                    sys.stderr.write(
                        f"Error calling __log__ on {type(value).__name__}: {exc}\n"
                    )
                else:
                    if isinstance(extracted, dict):
                        for sub_key, sub_value in extracted.items():
                            try:
                                processed[normalize_context_key(sub_key)] = sub_value
                            except Exception as exc:  # noqa: BLE001
                                sys.stderr.write(
                                    f"Error normalizing context key {sub_key!r}: {exc}\n"  # noqa: E501
                                )
                    else:
                        sys.stderr.write(
                            f"__log__ must return dict, got {type(extracted).__name__}\n"  # noqa: E501
                        )
                continue

            with suppress(Exception):
                processed[normalize_context_key(key)] = value

        merged.update(processed)
        return merged

    def _create_record(
        self,
        level: LevelType | str,
        message: str | Callable[[], str],
        tags: set[str],
        context: dict[str, Any],
        *,
        stacklevel: int = 2,
    ) -> Record:
        if isinstance(level, str):
            level = Level.get_by_name(normalize_level_name(level)) or Level.NOTSET
        frame = sys._getframe(stacklevel)
        code = frame.f_code
        logger = cast("Logger", self)
        return Record(
            message=message,
            level=level,
            logger=logger,
            logger_id=logger._logger_id,
            trace_id=logger._generate_trace_id(),
            file=code.co_filename,
            function=code.co_name,
            line=frame.f_lineno,
            context=context,
            tags=tags,
        )

    def _apply_processors_start(
        self,
        processors: ProcessorsManager,
        record: Record,
    ) -> Record | None:
        for processor in processors:
            try:
                result = processor.start(record.copy())
                if result is None:
                    return None
                record = result
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write(
                    f"Exception in {processor.__class__.__name__}.start: {exc}\n"
                )
        return record

    def _apply_processors_end(
        self,
        processors: ProcessorsManager,
        record: Record,
    ) -> Record | None:
        for processor in reversed(processors):
            try:
                result = processor.end(record.copy())
                if result is None:
                    return None
                record = result
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write(
                    f"Exception in {processor.__class__.__name__}.end: {exc}\n"
                )
        return record

    def _apply_handlers(
        self,
        handlers: HandlersManager,
        record: Record,
    ) -> None:
        for handler in handlers:
            try:
                handler.handle(record)
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write(
                    f"Exception in {handler.__class__.__name__}.handle: {exc}\n"
                )

    def _apply_filters(
        self,
        filters: FiltersManager,
        record: Record,
        *,
        enabled: bool,
    ) -> Record | None:
        if enabled and not all(f.filter(record) for f in filters):
            return None
        return record

    def _process_global(self, record: Record) -> Record | None:
        glob = self._container.globals

        if not glob.status.logger.enabled:
            return None
        if not record.level.passed_level(glob.level.get()):
            return None

        processed = self._apply_processors_start(glob.processors, record)
        if processed is None:
            return None
        record = processed

        filtered = self._apply_filters(
            glob.filters,
            record,
            enabled=self.status.global_filters.enabled,
        )
        if filtered is None:
            return None
        record = filtered

        if self.status.global_handlers.enabled:
            self._apply_handlers(glob.handlers, record)

        return self._apply_processors_end(glob.processors, record)

    def _process_local(self, record: Record) -> Record | None:
        if not self.status.logger.enabled:
            return None
        if not record.level.passed_level(self.level.get()):
            return None

        processed = self._apply_processors_start(self.processors, record)
        if processed is None:
            return None
        record = processed

        filtered = self._apply_filters(
            self.filters,
            record,
            enabled=self.status.filters.enabled,
        )
        if filtered is None:
            return None
        record = filtered

        if self.status.handlers.enabled:
            self._apply_handlers(self.handlers, record)

        return self._apply_processors_end(self.processors, record)

    def _process_record(self, record: Record) -> Record | None:
        result = self._process_local(record)
        if result is None:
            return None
        record = result

        current = self
        while current.propagate and current is not current.parent:
            current = current.parent
            parent_result = current._process_local(record)
            if parent_result is None:
                break
            record = parent_result

        self.metrics.add(record.level)
        return record
