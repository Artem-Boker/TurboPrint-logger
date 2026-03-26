from __future__ import annotations

from abc import ABC, abstractmethod

from turboprint_logger.core.record import Record

__all__ = ("Processor",)


class Processor(ABC):
    __slots__ = ()

    @abstractmethod
    def process(self, record: Record) -> Record | None:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
