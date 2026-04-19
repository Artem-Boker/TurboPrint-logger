from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock, local

from turboprint_logger.interfaces import Filter

__all__ = ("FiltersManager",)


class FiltersManager:
    __slots__ = ("_filters", "_lock", "_thread_local")

    def __init__(self, *filters: Filter) -> None:
        self._lock = RLock()
        self._filters = list(filters)
        self._thread_local = local()

    def get(self) -> tuple[Filter, ...]:
        with self._lock:
            return tuple(self._filters)

    def add(self, *filters: Filter) -> None:
        with self._lock:
            self._filters.extend(filters)

    def remove(self, filter: Filter) -> bool:  # noqa: A002
        try:
            with self._lock:
                self._filters.remove(filter)
        except ValueError:
            return False
        return True

    def clear(self) -> None:
        with self._lock:
            self._filters.clear()

    @contextmanager
    def temporary(self, *filters: Filter, replace: bool = True):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._filters.copy()
            self._thread_local.stack.append(snapshot)
            self._filters = list(filters) if replace else [*self._filters, *filters]

            try:
                yield
            finally:
                self._filters = self._thread_local.stack.pop()

    def __len__(self) -> int:
        with self._lock:
            return len(self._filters)

    def __iter__(self) -> Iterator[Filter]:
        with self._lock:
            return iter(self._filters)

    def __getitem__(self, index: int) -> Filter:
        with self._lock:
            return self._filters[index]

    def __contains__(self, filter: Filter) -> bool:  # noqa: A002
        with self._lock:
            return filter in self._filters

    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._filters)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(filters_count={len(self._filters)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filters={self._filters})"
