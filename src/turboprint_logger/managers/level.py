from __future__ import annotations

from contextlib import contextmanager
from threading import Lock

from turboprint_logger.core.levels import Level, Level

__all__ = ("LevelManager",)


class LevelManager:
    __slots__ = ("_level", "_lock")

    def __init__(self, level: Level | None = None) -> None:
        self._lock = Lock()
        self._level: Level = level or Level.NOTSET

    def get(self) -> Level:
        with self._lock:
            return self._level

    def set(self, level: Level) -> None:
        with self._lock:
            self._level = level

    @contextmanager
    def temporary(self, level: Level):  # noqa: ANN201
        with self._lock:
            original = self._level
            self._level = level
        try:
            yield
        finally:
            with self._lock:
                self._level = original

    def enabled_for(self, level: Level) -> bool:
        with self._lock:
            return self._level.enabled_for(level)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(level_name={self._level.name})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(level={self._level!r})"
