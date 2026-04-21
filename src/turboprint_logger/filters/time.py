from __future__ import annotations

from datetime import UTC, datetime, time

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("TimeFilter",)


class TimeFilter(Filter):
    def __init__(
        self,
        start: time | None = None,
        end: time | None = None,
    ) -> None:
        self.start = start
        self.end = end

    def filter(self, record: Record) -> bool:
        current_date = datetime.now(UTC).date()
        record_time = record.date_time.astimezone(UTC).time()
        start = (
            datetime.combine(current_date, self.start).astimezone(UTC).time()
            if self.start
            else None
        )
        end = (
            datetime.combine(current_date, self.end).astimezone(UTC).time()
            if self.end
            else None
        )

        if start is not None and end is not None and start > end:
            if record_time < end:
                return True
            return record_time >= start

        if start and record_time < start:
            return False
        return not (end and record_time > end)
