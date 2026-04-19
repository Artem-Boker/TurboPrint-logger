from __future__ import annotations

from contextlib import contextmanager
from threading import RLock, local

from turboprint_logger.core.levels import Level, LevelRegistry

__all__ = ("LevelManager",)


class LevelManager:
    __slots__ = ("_level", "_lock", "_thread_local")

    def __init__(self, level: LevelRegistry | None = None) -> None:
        self._lock = RLock()
        self._level = level or Level.NOTSET
        self._thread_local = local()

    def get(self) -> LevelRegistry:
        with self._lock:
            return self._level

    def set(self, level: LevelRegistry) -> None:
        with self._lock:
            self._level = level

    @contextmanager
    def temporary(self, level: LevelRegistry):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._level
            self._thread_local.stack.append(snapshot)
            self._level = level

            try:
                yield
            finally:
                self._level = self._thread_local.stack.pop()

    def passed_min_level(self, level: LevelRegistry) -> bool:
        with self._lock:
            return self._level.passed_min_level(level)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(level_name={self._level.name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(level={self._level!r})"
