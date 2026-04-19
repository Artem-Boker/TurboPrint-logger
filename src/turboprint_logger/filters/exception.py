from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("ExceptionFilter",)


class ExceptionFilter(Filter):
    def __init__(
        self,
        exception_types: list[type[BaseException]] | None = None,
        *,
        include: bool = True,
    ) -> None:
        self.include = include
        self.exception_types = exception_types

    def filter(self, record: Record) -> bool:
        if record.exception_info[0] is None or self.exception_types is None:
            matches = False
        else:
            exc_type = record.exception_info[0]
            matches = any(issubclass(exc_type, et) for et in self.exception_types)

        if self.include:
            return matches
        return not matches
