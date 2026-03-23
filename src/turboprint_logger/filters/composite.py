from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("CompositeFilter",)


class CompositeFilter(Filter):
    def __init__(self, *filters: Filter, all_filters: bool = True) -> None:
        self.filters = filters
        self.check = all if all_filters else any

    def filter(self, record: Record) -> bool:
        return self.check(f.filter(record) for f in self.filters)
