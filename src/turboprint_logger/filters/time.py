from __future__ import annotations

from datetime import UTC, time

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("TimeFilter",)


class TimeFilter(Filter):
    def __init__(self, start: time | None = None, end: time | None = None) -> None:
        self.start = start.replace(tzinfo=UTC) if start else None
        self.end = end.replace(tzinfo=UTC) if end else None

    def filter(self, record: Record) -> bool:
        record_time = record.date_time.time().replace(tzinfo=UTC)
        if self.start and record_time < self.start:
            return False
        return not (self.end and record_time > self.end)
