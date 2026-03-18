from __future__ import annotations

from abc import ABC, abstractmethod

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter, Formatter


class Handler(ABC):
    __slots__ = ("filters", "formatter", "level")

    def __init__(
        self,
        min_level: LevelRegistry = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        self.level = min_level
        self.formatter = formatter
        self.filters = filters or []

    def handle(self, record: Record) -> None:
        if record.level.level >= self.level.level and all(
            f.filter(record) for f in self.filters
        ):
            self.emit(record)

    @abstractmethod
    def emit(self, record: Record) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"min_level={self.level}, "
            f"formatter={self.formatter}, "
            f"filters={tuple(self.filters)})"
        )
