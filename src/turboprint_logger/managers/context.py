from __future__ import annotations

from collections.abc import Iterable
from contextlib import contextmanager
from threading import Lock
from typing import Any

from turboprint_logger.utils.normalizers import normalize_context_key

__all__ = ("ContextManager",)


class ContextManager:
    __slots__ = ("_context", "_lock")

    def __init__(self, **context) -> None:
        self._lock = Lock()
        self._context: dict[str, Any] = context

    def get(self) -> dict[str, Any]:
        with self._lock:
            return self._context

    def copy(self) -> dict[str, Any]:
        with self._lock:
            return self._context.copy()

    def clear(self) -> None:
        with self._lock:
            self._context.clear()

    def update(self, **context) -> None:
        with self._lock:
            self._context.update(context)

    @contextmanager
    def temporary(self, *, replace: bool = True, **context):  # noqa: ANN201
        with self._lock:
            original = self._context
            self._context = context if replace else {**self._context, **context}
        try:
            yield
        finally:
            with self._lock:
                self._context = original

    def values(self) -> Iterable[Any]:
        with self._lock:
            return self._context.values()

    def keys(self) -> Iterable[Any]:
        with self._lock:
            return self._context.keys()

    def items(self) -> Iterable[tuple[str, Any]]:
        with self._lock:
            return self._context.items()

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        key = normalize_context_key(key)
        with self._lock:
            return self._context[key]

    def __delitem__(self, key: str) -> None:
        key = normalize_context_key(key)
        with self._lock:
            del self._context[key]

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        key = normalize_context_key(key)
        with self._lock:
            self._context[key] = value

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(context_keys={self.keys()})"
