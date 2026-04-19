from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock, local

from turboprint_logger.interfaces import Handler

__all__ = ("HandlersManager",)


class HandlersManager:
    __slots__ = ("_handlers", "_lock", "_thread_local")

    def __init__(self, *handlers: Handler) -> None:
        self._lock = RLock()
        self._handlers = list(handlers)
        self._thread_local = local()

    def get(self) -> tuple[Handler, ...]:
        with self._lock:
            return tuple(self._handlers)

    def add(self, *handlers: Handler) -> None:
        with self._lock:
            self._handlers.extend(handlers)

    def remove(self, handler: Handler) -> bool:
        try:
            with self._lock:
                self._handlers.remove(handler)
        except ValueError:
            return False
        return True

    def clear(self) -> None:
        with self._lock:
            self._handlers.clear()

    @contextmanager
    def temporary(self, *handlers: Handler, replace: bool = True):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._handlers.copy()
            self._thread_local.stack.append(snapshot)
            self._handlers = list(handlers) if replace else [*self._handlers, *handlers]

            try:
                yield
            finally:
                self._handlers = self._thread_local.stack.pop()

    def __len__(self) -> int:
        with self._lock:
            return len(self._handlers)

    def __iter__(self) -> Iterator[Handler]:
        with self._lock:
            return iter(self._handlers.copy())

    def __getitem__(self, index: int) -> Handler:
        with self._lock:
            return self._handlers[index]

    def __contains__(self, handler: Handler) -> bool:
        with self._lock:
            return handler in self._handlers

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(handlers_count={len(self._handlers)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(handlers={self._handlers})"
