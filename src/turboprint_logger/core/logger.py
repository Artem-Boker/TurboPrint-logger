from __future__ import annotations

import sys
from collections.abc import Callable
from threading import Lock, RLock
from typing import Any

from turboprint_logger.core.config import Config
from turboprint_logger.core.container import Container, get_default_container
from turboprint_logger.core.levels import Level, Level
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.core.logger import LoggerInstantiationError
from turboprint_logger.managers.context import ContextManager
from turboprint_logger.managers.filters import FiltersManager
from turboprint_logger.managers.formatter import FormatterManager
from turboprint_logger.managers.handlers import HandlersManager
from turboprint_logger.managers.level import LevelManager
from turboprint_logger.managers.metrics import MetricsManager
from turboprint_logger.managers.processors import ProcessorsManager
from turboprint_logger.managers.status import StatusManager
from turboprint_logger.managers.tags import TagsManager
from turboprint_logger.utils.normalizers import (
    normalize_context_key,
    normalize_logger_name,
)

__all__ = ("Logger",)


_ROOT_LOGGER_NAME = "root".strip().lower()
_DEFAULT_CONTAINER = get_default_container()


class Logger:
    __slots__ = (
        "__weakref__",
        "_container",
        "_logger_id",
        "_name",
        "context",
        "filters",
        "formatter",
        "handlers",
        "level",
        "metrics",
        "parent",
        "processors",
        "propagate",
        "status",
        "tags",
    )
    _get_logger_lock = RLock()
    _trace_counter = 0
    _trace_counter_lock = Lock()
    _logger_counter = 0
    _logger_counter_lock = Lock()

    def __init__(self) -> None:
        self._name: str
        self._logger_id: int
        self._container: Container
        self.parent: Logger
        self.propagate: bool
        self.level: LevelManager
        self.formatter: FormatterManager
        self.processors: ProcessorsManager
        self.handlers: HandlersManager
        self.filters: FiltersManager
        self.context: ContextManager
        self.tags: TagsManager
        self.metrics: MetricsManager
        self.status: StatusManager
        msg = "Logger cannot be instantiated directly. Use Logger.get_logger()"
        raise LoggerInstantiationError(msg)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def _create(
        cls, name: str, container: Container, config: Config | None = None
    ) -> Logger:
        config = config or Config()
        self = super().__new__(cls)
        self._logger_id = self._next_logger_id()
        self._container = container

        if name != _ROOT_LOGGER_NAME:
            parent_name = name.rsplit(".", 1)[0] if "." in name else _ROOT_LOGGER_NAME
            self.parent = Logger.get_logger(parent_name, container=container)
        else:
            self.parent = self

        self._name = name
        self.propagate = (
            config.propagate
            if config.propagate is not None
            else container.defaults.propagate
        )

        self._create_managers(config)

        if name != _ROOT_LOGGER_NAME:
            self._container._loggers[name] = self
        return self

    def _create_managers(self, config: Config) -> None:
        defaults = self._container.defaults

        self.level = LevelManager(config.min_level or defaults.level.get())
        self.formatter = FormatterManager(config.formatter or defaults.formatter.get())
        self.processors = ProcessorsManager(
            *(config.processors or defaults.processors.get())
        )
        self.handlers = HandlersManager(*(config.handlers or defaults.handlers.get()))
        self.filters = FiltersManager(*(config.filters or defaults.filters.get()))
        self.context = ContextManager(**(config.context or defaults.context.get()))
        self.tags = TagsManager(*(config.tags or defaults.tags.get()))
        self.metrics = MetricsManager()
        logger_status = (
            config.status
            if config.status is not None
            else defaults.status.logger.enabled
        )
        self.status = StatusManager(
            logger=logger_status,
            handlers=defaults.status.handlers.enabled,
            filters=defaults.status.filters.enabled,
            global_handlers=defaults.status.global_handlers.enabled,
            global_filters=defaults.status.global_filters.enabled,
        )

    @classmethod
    def _next_logger_id(cls) -> int:
        with cls._logger_counter_lock:
            cls._logger_counter += 1
            return cls._logger_counter

    @classmethod
    def _generate_trace_id(cls) -> int:
        with cls._trace_counter_lock:
            cls._trace_counter += 1
            return cls._trace_counter

    @classmethod
    def get_logger(
        cls,
        name: str = _ROOT_LOGGER_NAME,
        config: Config | None = None,
        container: Container = _DEFAULT_CONTAINER,
    ) -> Logger:
        name = normalize_logger_name(name)
        with cls._get_logger_lock:
            if not container._root_logger:
                container._root_logger = Logger._create(
                    _ROOT_LOGGER_NAME, container, None
                )
            if name == _ROOT_LOGGER_NAME:
                return container._root_logger
            existing = container._loggers.get(name)
            if existing is None:
                logger = Logger._create(name, container, config)
                container._loggers[name] = logger
                return logger
            return existing

    def _merge_tags(self, tags: list[str] | None = None) -> set[str]:
        merged_tags = set()
        merged_tags.update(self._container.globals.tags.get())
        merged_tags.update(self.tags.get())
        merged_tags.update(tags or [])
        return merged_tags

    def _merge_context(self, extra: dict[str, Any]) -> dict[str, Any]:
        merged_context = {}
        merged_context.update(self._container.globals.context.get())
        merged_context.update(self.context.get())
        merged_context.update(
            {normalize_context_key(key): value for key, value in extra.items()}
        )
        return merged_context

    def _create_record(
        self,
        level: Level | str,
        message: str | Callable[[], str],
        tags: set[str],
        context: dict[str, Any],
        *,
        stacklevel: int = 2,
    ) -> Record:
        if isinstance(level, str):
            level = Level.get_by_name(level) or Level.NOTSET
        frame = sys._getframe(stacklevel)
        code = frame.f_code
        return Record(
            message=message,
            level=level,
            logger=self,
            logger_id=self._logger_id,
            trace_id=self._generate_trace_id(),
            file=code.co_filename,
            function=code.co_name,
            line=frame.f_lineno,
            context=context,
            tags=tags,
        )

    def _process_global(self, record: Record) -> Record | None:
        if not self._container.globals.status.logger.enabled:
            return None

        if not record.level.enabled_for(self._container.globals.level.get()):
            return None

        for processor in self._container.globals.processors:
            try:
                processed_record = processor.process(record)
                if processed_record:
                    record = processed_record
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write(
                    f"Exception in {processor.__class__.__name__}: {exc}\n"
                )

        if self.status.global_filters.enabled and not all(
            f.filter(record) for f in self._container.globals.filters
        ):
            return None

        if self.status.global_handlers.enabled:
            for handler in self._container.globals.handlers:
                try:
                    handler.handle(record)
                except Exception as exc:  # noqa: BLE001
                    sys.stderr.write(
                        f"Exception in {handler.__class__.__name__}: {exc}\n"
                    )

        return record

    def _process_local(self, record: Record) -> Record | None:
        if not self.status.logger.enabled:
            return None

        if not record.level.enabled_for(self.level.get()):
            return None

        for processor in self.processors:
            try:
                processed_record = processor.process(record)
                if processed_record:
                    record = processed_record
            except Exception as exc:  # noqa: BLE001
                sys.stderr.write(
                    f"Exception in {processor.__class__.__name__}: {exc}\n"
                )

        if self.status.filters.enabled and not all(
            f.filter(record) for f in self.filters
        ):
            return None

        if self.status.handlers.enabled:
            for handler in self.handlers:
                try:
                    handler.handle(record)
                except Exception as exc:  # noqa: BLE001
                    sys.stderr.write(
                        f"Exception in {handler.__class__.__name__}: {exc}\n"
                    )

        return record

    def _process_record(self, record: Record) -> Record:
        current = self
        while current:
            current_record = current._process_local(record)
            if not current_record:
                return record
            record = current_record
            if not current.propagate or current is current.parent:
                break
            current = current.parent
        self.metrics.add(record.level)
        return record

    def __call__(
        self,
        level: Level | str,
        message: str | Callable[[], str],
        *,
        tags: list[str] | None = None,
        **extra,
    ) -> Record:
        merged_tags = self._merge_tags(tags)
        merged_context = self._merge_context(extra)
        record = self._create_record(level, message, merged_tags, merged_context)
        record = self._process_global(record)
        if record:
            record = self._process_record(record)
        return record

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f'name="{self.name}", '
            f"logger_id={self._logger_id}, "
            f'container_name="{self._container.name}", '
            f"propagate={self.propagate}, "
            f"min_level={self.level.get()!r}, "
            f"formatter={self.formatter.get()}, "
            f"filters={self.filters.get()}, "
            f"handlers={self.handlers.get()}, "
            f"context_keys={tuple(self.context.keys())}, "
            f"tags={tuple(self.tags.get())}, "
            f"status={self.status})"
        )
