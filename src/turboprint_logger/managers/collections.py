from __future__ import annotations

from typing import Any

from turboprint_logger.core.levels import Level
from turboprint_logger.interfaces import Filter, Formatter, Handler
from turboprint_logger.interfaces.processor import Processor
from turboprint_logger.managers.context import ContextManager
from turboprint_logger.managers.filters import FiltersManager
from turboprint_logger.managers.formatter import FormatterManager
from turboprint_logger.managers.handlers import HandlersManager
from turboprint_logger.managers.level import LevelManager
from turboprint_logger.managers.processors import ProcessorsManager
from turboprint_logger.managers.status import StatusManager
from turboprint_logger.managers.tags import TagsManager

__all__ = ("DefaultManager", "GlobalManager")


class ManagerCollection:
    __slots__ = (
        "context",
        "filters",
        "formatter",
        "handlers",
        "level",
        "processors",
        "propagate",
        "status",
        "tags",
    )

    def __init__(  # noqa: PLR0913
        self,
        level: Level | None = None,
        formatter: Formatter | None = None,
        processors: list[Processor] | None = None,
        handlers: list[Handler] | None = None,
        filters: list[Filter] | None = None,
        context: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        *,
        logger_propagate: bool = True,
        logger_status: bool | None = None,
    ) -> None:
        self.level = LevelManager(level)
        self.formatter = FormatterManager(formatter)
        self.processors = ProcessorsManager(*(processors or ()))
        self.handlers = HandlersManager(*(handlers or ()))
        self.filters = FiltersManager(*(filters or ()))
        self.context = ContextManager(**(context or {}))
        self.tags = TagsManager(*(tags or ()))
        self.status = StatusManager(
            logger=logger_status if logger_status is not None else True
        )
        self.propagate = logger_propagate

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"level={self.level!r}, "
            f"formatter={self.formatter!r}, "
            f"processors_count={len(self.processors)}, "
            f"handlers_count={len(self.handlers)}, "
            f"filters_count={len(self.filters)}, "
            f"context_keys={self.context.keys()}, "
            f"tags_count={len(self.tags)}, "
            f"status={self.status})"
        )


class GlobalManager(ManagerCollection):
    pass


class DefaultManager(ManagerCollection):
    pass
