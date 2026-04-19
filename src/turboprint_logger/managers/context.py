from __future__ import annotations

from contextlib import contextmanager
from threading import RLock, local
from typing import Any

from turboprint_logger.utils.normalizers import normalize_context_key

__all__ = ("ContextManager",)


class ContextManager:
    __slots__ = ("_context", "_lock", "_thread_local")

    def __init__(self, **context) -> None:
        self._lock = RLock()
        self._context: dict[str, Any] = {
            normalize_context_key(key): value for key, value in context.items()
        }
        self._thread_local = local()

    def get(self) -> dict[str, Any]:
        with self._lock:
            return self._context.copy()

    def clear(self) -> None:
        with self._lock:
            self._context.clear()

    def update(self, **context) -> None:
        with self._lock:
            self._context.update(
                {normalize_context_key(key): value for key, value in context.items()}
            )

    @contextmanager
    def temporary(self, *, replace: bool = True, **context):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        normalized = {
            normalize_context_key(key): value for key, value in context.items()
        }

        with self._lock:
            snapshot = self._context.copy()
            self._thread_local.stack.append(snapshot)
            self._context = normalized if replace else {**self._context, **normalized}

            try:
                yield
            finally:
                self._context = self._thread_local.stack.pop()

    def values(self) -> list[Any]:
        with self._lock:
            return list(self._context.values())

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._context.keys())

    def items(self) -> list[tuple[str, Any]]:
        with self._lock:
            return list(self._context.items())

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
