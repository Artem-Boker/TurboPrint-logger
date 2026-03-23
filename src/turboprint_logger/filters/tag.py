from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("TagFilter",)


class TagFilter(Filter):
    def __init__(self, *required_tags: str, match_all: bool = True) -> None:
        self.required = required_tags
        self.check = all if match_all else any

    def filter(self, record: Record) -> bool:
        return self.check(tag in record.tags for tag in self.required)
