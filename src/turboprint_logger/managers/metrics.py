from __future__ import annotations

from collections import Counter
from threading import Lock

from turboprint_logger.core.levels import Level, LevelType

__all__ = ("MetricsManager",)


class MetricsManager:
    __slots__ = ("_lock", "_metrics")

    def __init__(self) -> None:
        self._lock = Lock()
        self._metrics: Counter[int] = Counter()

    def get(self) -> dict[int, int]:
        with self._lock:
            return self._metrics.copy()

    def add(self, level: LevelType) -> None:
        with self._lock:
            self._metrics[level.value] += 1

    def subtract(self, level: LevelType) -> bool:
        with self._lock:
            key = level.value
            if key not in self._metrics:
                return False
            if self._metrics.get(key, 0) <= 1:
                del self._metrics[key]
                return True
            self._metrics[key] -= 1
            return True

    def total(self) -> int:
        with self._lock:
            return self._metrics.total()

    def items(self) -> dict[LevelType, int]:
        with self._lock:
            result = {}
            for level_int, count in self._metrics.items():
                level = Level.get_by_level(level_int)
                if level:
                    result[level] = count
            return result

    def reset(self, level: LevelType | None = None) -> None:
        with self._lock:
            if level is not None:
                self._metrics.pop(level.value, 0)
            else:
                self._metrics.clear()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(total_metrics={self.total()})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(metrics={self.items()}, total={self.total()})"
        )
