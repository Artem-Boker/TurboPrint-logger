from __future__ import annotations

from abc import ABC, abstractmethod

from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.interfaces import InterfaceMethodNotImplementedError

__all__ = ("Processor",)


class Processor(ABC):
    __slots__ = ()

    @abstractmethod
    def process(self, record: Record) -> Record | None:
        msg = "Processor.process must be implemented by subclasses"
        raise InterfaceMethodNotImplementedError(msg)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
