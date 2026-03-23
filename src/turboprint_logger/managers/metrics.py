from __future__ import annotations

from collections import Counter
from threading import Lock

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.exceptions.managers.metrics import NegativeMetricsCountError

__all__ = ("MetricsManager",)


class MetricsManager:
    __slots__ = ("_lock", "_metrics")

    def __init__(self) -> None:
        self._lock = Lock()
        self._metrics: Counter[int] = Counter()

    def get(self) -> dict[int, int]:
        with self._lock:
            return self._metrics

    def add(self, level: LevelRegistry) -> None:
        with self._lock:
            self._metrics[level.level] += 1

    def subtract(self, level: LevelRegistry) -> bool:
        with self._lock:
            key = level.level
            if key not in self._metrics:
                return False
            if self._metrics.get(key, 0) <= 1:
                del self._metrics[key]
                return False
            self._metrics[key] -= 1
            return True

    def total(self) -> int:
        with self._lock:
            return self._metrics.total()

    def items(self) -> dict[LevelRegistry, int]:
        with self._lock:
            result = {}
            for level_int, count in self._metrics.items():
                level = Level.get_by_level(level_int)
                if level:
                    result[level] = count
            return result

    def reset(self, level: LevelRegistry | None = None) -> None:
        with self._lock:
            if level:
                self._metrics.pop(level.level, 0)
            else:
                self._metrics.clear()

    def __getitem__(self, level: LevelRegistry) -> int:
        with self._lock:
            return self._metrics.get(level.level, 0)

    def __delitem__(self, level: LevelRegistry) -> None:
        with self._lock:
            del self._metrics[level.level]

    def __setitem__(self, level: LevelRegistry, count: int) -> None:
        if count < 0:
            msg = f"Metrics count cannot be negative, got {count}"
            raise NegativeMetricsCountError(msg)
        with self._lock:
            self._metrics[level.level] = count

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(total_metrics={self.total()})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(metrics={self.items()}, total={self.total()})"
        )
