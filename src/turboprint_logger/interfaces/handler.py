from __future__ import annotations

from abc import ABC, abstractmethod
from weakref import finalize

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.interfaces import InterfaceMethodNotImplementedError
from turboprint_logger.interfaces import Filter, Formatter

__all__ = ("Handler",)


class Handler(ABC):
    __slots__ = ("_finalizer", "filters", "formatter", "level")

    def __init__(
        self,
        level: LevelType = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        self.level = level
        self.formatter = formatter
        self.filters = filters or []
        self._finalizer = finalize(self, self.close)

    def handle(self, record: Record) -> None:
        if record.level.value >= self.level.value and all(
            f.filter(record) for f in self.filters
        ):
            self.emit(record)

    @abstractmethod
    def emit(self, record: Record) -> None:
        msg = "Handler.emit must be implemented by subclasses"
        raise InterfaceMethodNotImplementedError(msg)

    @abstractmethod
    def close(self) -> None:
        msg = "Handler.close must be implemented by subclasses"
        raise InterfaceMethodNotImplementedError(msg)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"level={self.level}, "
            f"formatter={self.formatter}, "
            f"filters={tuple(self.filters)})"
        )
