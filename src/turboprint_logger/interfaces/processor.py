from __future__ import annotations

from abc import ABC

from turboprint_logger.core.record import Record

__all__ = ("Processor",)


class Processor(ABC):  # noqa: B024
    __slots__ = ()

    def start(self, record: Record) -> Record | None:
        return record

    def end(self, record: Record) -> Record | None:
        return record

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
