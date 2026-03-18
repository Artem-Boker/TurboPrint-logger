from __future__ import annotations

from abc import ABC, abstractmethod

from turboprint_logger.core.record import Record


class Formatter(ABC):
    __slots__ = ()

    @abstractmethod
    def format(self, record: Record) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
