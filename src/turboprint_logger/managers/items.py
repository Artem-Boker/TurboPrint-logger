from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock, local
from typing import Any, Generic, TypeVar

from turboprint_logger.interfaces import Filter, Handler, Processor
from turboprint_logger.utils.normalizers import normalize_context_key

__all__ = ()

T = TypeVar("T")


class CollectionManager(Generic[T]):
    __slots__ = ("_items", "_lock", "_thread_local")

    def __init__(self, *items: T) -> None:
        self._lock = RLock()
        self._items = list(items)
        self._thread_local = local()

    def get(self) -> tuple[T, ...]:
        with self._lock:
            return tuple(self._items)

    def add(self, *items: T) -> None:
        with self._lock:
            self._items.extend(items)

    def remove(self, item: T) -> bool:
        try:
            with self._lock:
                self._items.remove(item)
        except ValueError:
            return False
        return True

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    @contextmanager
    def temporary(self, *items: T, replace: bool = True):  # noqa: ANN202
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._items.copy()
            self._thread_local.stack.append(snapshot)
            self._items = list(items) if replace else [*self._items, *items]

            try:
                yield
            finally:
                self._items = self._thread_local.stack.pop()

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)

    def __iter__(self) -> Iterator[T]:
        with self._lock:
            return iter(self._items.copy())

    def __getitem__(self, index: int) -> T:
        with self._lock:
            return list(self._items)[index]

    def __contains__(self, item: T) -> bool:
        with self._lock:
            return item in self._items

    def __bool__(self) -> bool:
        with self._lock:
            return bool(self._items)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(filters_count={len(self._items)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self._items!r})"


class FiltersManager(CollectionManager[Filter]):
    pass


class HandlersManager(CollectionManager[Handler]):
    pass


class ProcessorsManager(CollectionManager[Processor]):
    pass


class TagsManager(CollectionManager[str]):
    def get(self) -> set[str]:  # ty:ignore[invalid-method-override]
        with self._lock:
            return set(self._items.copy())


class ContextManager:
    __slots__ = ("_items", "_lock", "_thread_local")

    def __init__(self, **items) -> None:
        self._lock = RLock()
        self._items: dict[str, Any] = {
            normalize_context_key(key): value for key, value in items.items()
        }
        self._thread_local = local()

    def get(self) -> dict[str, Any]:
        with self._lock:
            return self._items.copy()

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def update(self, **items) -> None:
        with self._lock:
            self._items.update(
                {normalize_context_key(key): value for key, value in items.items()}
            )

    @contextmanager
    def temporary(self, *, replace: bool = True, **items):  # noqa: ANN202
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        normalized = {normalize_context_key(key): value for key, value in items.items()}

        with self._lock:
            snapshot = self._items.copy()
            self._thread_local.stack.append(snapshot)
            self._items = normalized if replace else {**self._items, **normalized}

            try:
                yield
            finally:
                self._items = self._thread_local.stack.pop()

    def values(self) -> list[Any]:
        with self._lock:
            return list(self._items.values())

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._items.keys())

    def items(self) -> list[tuple[str, Any]]:
        with self._lock:
            return list(self._items.items())

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        return iter(self._items.items())

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        key = normalize_context_key(key)
        with self._lock:
            return self._items[key]

    def __delitem__(self, key: str) -> None:
        key = normalize_context_key(key)
        with self._lock:
            del self._items[key]

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        key = normalize_context_key(key)
        with self._lock:
            self._items[key] = value

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self.keys()})"
