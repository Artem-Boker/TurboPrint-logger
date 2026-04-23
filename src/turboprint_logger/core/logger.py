from __future__ import annotations

from collections.abc import Callable

from turboprint_logger.core._logger_factory import _LoggerFactory
from turboprint_logger.core._logger_pipeline import _LoggerPipeline
from turboprint_logger.core.config import Config
from turboprint_logger.core.levels import LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.utils.normalizers import normalize_logger_name

__all__ = ("Logger",)


class Logger(_LoggerFactory, _LoggerPipeline):
    def __call__(
        self,
        level: LevelType | str,
        message: str | Callable[[], str],
        *,
        tags: list[str] | None = None,
        stacklevel: int = 2,
        **extra,
    ) -> Record | None:
        merged_tags = self._merge_tags(tags)
        merged_context = self._merge_context(extra)
        record = self._create_record(
            level,
            message,
            merged_tags,
            merged_context,
            stacklevel=stacklevel,
        )
        processed = self._process_global(record)
        if processed is None:
            return None
        return self._process_record(processed)

    def configure(self, config: Config) -> None:
        if config.level is not None:
            self.level.set(config.level)

        if config.formatter is not None:
            self.formatter.set(config.formatter)

        if config.processors is not None:
            self.processors.clear()
            self.processors.add(*config.processors)

        if config.handlers is not None:
            self.handlers.clear()
            self.handlers.add(*config.handlers)

        if config.filters is not None:
            self.filters.clear()
            self.filters.add(*config.filters)

        if config.context is not None:
            self.context.clear()
            self.context.update(**config.context)

        if config.tags is not None:
            self.tags.clear()
            self.tags.add(*config.tags)

        if config.propagate is not None:
            self.propagate = config.propagate

        if config.status is not None:
            self.status.logger.set(config.status)

    def get_child(self, suffix: str) -> Logger:
        child_name = normalize_logger_name(f"{self._name}.{suffix.strip('.')}")
        return Logger.get_logger(child_name, container=self._container)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f'name="{self.name}", '
            f"logger_id={self._logger_id}, "  # ty:ignore[unresolved-attribute]
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
