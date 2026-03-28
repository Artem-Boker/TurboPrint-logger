from __future__ import annotations

from abc import ABC, abstractmethod

from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.interfaces import InterfaceMethodNotImplementedError

__all__ = ("Filter",)


class Filter(ABC):
    __slots__ = ()

    @abstractmethod
    def filter(self, record: Record) -> bool:
        msg = "Filter.filter must be implemented by subclasses"
        raise InterfaceMethodNotImplementedError(msg)

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
