from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("TagFilter",)


class TagFilter(Filter):
    def __init__(
        self, *required_tags: str, match_all: bool = True, opposite: bool = False
    ) -> None:
        self.required = required_tags
        self.check = all if match_all else any
        self.opposite = opposite

    def filter(self, record: Record) -> bool:
        if not self.required:
            return True

        result = self.check(tag in record.tags for tag in self.required)

        if self.opposite:
            return not result
        return result
