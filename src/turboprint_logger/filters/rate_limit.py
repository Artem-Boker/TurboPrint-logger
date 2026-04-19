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
        self.rate = max(0.0, rate)
        self.per = max(0.0, per)
        self.capacity = float(burst if burst is not None else max(1, int(rate)))
        self.key = key
        self._buckets: dict[str, tuple[float, float]] = {}
        self._lock = Lock()
        self._evict_after = (
            (self.capacity / self.rate * self.per * 2) if self.rate > 0 else 3600.0
        )

    def filter(self, record: Record) -> bool:
        key = self._get_key(record)
        now = time()
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = (self.capacity - 1.0, now)
                return True

            tokens, last_ts = self._buckets[key]

            if self.per > 0:
                elapsed = now - last_ts
                refill = elapsed * (self.rate / self.per)
                tokens = min(self.capacity, tokens + refill)

            if tokens >= self.capacity and (now - last_ts) > self._evict_after:
                del self._buckets[key]
                self._buckets[key] = (self.capacity - 1.0, now)
                return True

            if tokens >= 1.0:
                self._buckets[key] = (tokens - 1.0, now)
                return True

            self._buckets[key] = (tokens, now)
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
