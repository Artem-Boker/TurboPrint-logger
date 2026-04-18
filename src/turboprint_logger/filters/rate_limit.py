from __future__ import annotations

from threading import Lock
from time import time

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("RateLimitFilter",)


class RateLimitFilter(Filter):
    def __init__(
        self,
        rate: float,
        per: float = 1.0,
        burst: int | None = None,
        key: str | None = None,
    ) -> None:
        self.rate = max(0, rate)
        self.per = max(0, per)
        self.capacity = burst if burst is not None else int(rate)
        self.key = key
        self._buckets: dict[str, float] = {}
        self._lock = Lock()

    def filter(self, record: Record) -> bool:
        key = self._get_key(record)
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = time()
                return True
            if time() - self._buckets[key] > self.per:
                self._buckets[key] = time()
                return True
            return False

    def _get_key(self, record: Record) -> str:
        if self.key is None:
            return "__default__"
        if self.key == "logger_name":
            return record.logger.name
        if self.key == "level":
            return record.level.name
        if self.key == "file":
            return record.file
        return self.key
