from __future__ import annotations

from contextlib import contextmanager
from threading import RLock, local
from typing import Generic, TypeVar

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.formatters import SimpleFormatter
from turboprint_logger.interfaces import Formatter

__all__ = ()

T = TypeVar("T")


class BaseManager(Generic[T]):
    __slots__ = ("_item", "_lock", "_thread_local")
    default: T

    def __init__(self, item: T | None = None) -> None:
        self._lock = RLock()
        self._item = item or self.default
        self._thread_local = local()

    def get(self) -> T:
        with self._lock:
            return self._item  # pyright: ignore[reportReturnType]

    def set(self, item: T) -> None:
        with self._lock:
            self._item = item

    @contextmanager
    def temporary(self, item: T):  # noqa: ANN202
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._item
            self._thread_local.stack.append(snapshot)
            self._item = item

            try:
                yield
            finally:
                self._item = self._thread_local.stack.pop()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(item={self._item!s})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(item={self._item!r})"


class LevelManager(BaseManager[LevelType]):
    default = Level.NOTSET

    def passed_level(self, item: LevelType) -> bool:
        with self._lock:
            return self._item.passed_level(  # pyright: ignore[reportAttributeAccessIssue]
                item
            )


class FormatterManager(BaseManager[Formatter]):
    default = SimpleFormatter()
