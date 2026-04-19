from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock, local

__all__ = ("TagsManager",)


class TagsManager:
    __slots__ = ("_lock", "_tags", "_thread_local")

    def __init__(self, *tags: str) -> None:
        self._lock = RLock()
        self._tags = set(tags)
        self._thread_local = local()

    def get(self) -> set[str]:
        with self._lock:
            return self._tags.copy()

    def add(self, *tags: str) -> None:
        with self._lock:
            self._tags.update(tags)

    def remove(self, tag: str) -> None:
        with self._lock:
            self._tags.discard(tag)

    def clear(self) -> None:
        with self._lock:
            self._tags.clear()

    @contextmanager
    def temporary(self, *tags: str, replace: bool = True):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._tags.copy()
            self._thread_local.stack.append(snapshot)
            self._tags = set(tags) if replace else {*self._tags, *tags}

            try:
                yield
            finally:
                self._tags = self._thread_local.stack.pop()

    def __len__(self) -> int:
        with self._lock:
            return len(self._tags)

    def __iter__(self) -> Iterator[str]:
        with self._lock:
            return iter(self._tags.copy())

    def __getitem__(self, index: int) -> str:
        with self._lock:
            return list(self._tags)[index]

    def __contains__(self, tag: str) -> bool:
        with self._lock:
            return tag in self._tags

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(tags_count={len(self)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tags={self.get()})"
