from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock, local

from turboprint_logger.interfaces import Processor

__all__ = ("ProcessorsManager",)


class ProcessorsManager:
    __slots__ = ("_lock", "_processors", "_thread_local")

    def __init__(self, *processors: Processor) -> None:
        self._lock = RLock()
        self._processors: list[Processor] = list(processors)
        self._thread_local = local()

    def get(self) -> tuple[Processor, ...]:
        with self._lock:
            return tuple(self._processors)

    def add(self, *processors: Processor) -> None:
        with self._lock:
            self._processors.extend(processors)

    def remove(self, processor: Processor) -> bool:
        try:
            with self._lock:
                self._processors.remove(processor)
        except ValueError:
            return False
        return True

    def clear(self) -> None:
        with self._lock:
            self._processors.clear()

    @contextmanager
    def temporary(self, *processors: Processor, replace: bool = True):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._processors.copy()
            self._thread_local.stack.append(snapshot)
            self._processors = (
                list(processors) if replace else [*self._processors, *processors]
            )

            try:
                yield
            finally:
                self._processors = self._thread_local.stack.pop()

    def __len__(self) -> int:
        with self._lock:
            return len(self._processors)

    def __iter__(self) -> Iterator[Processor]:
        with self._lock:
            return iter(self._processors.copy())

    def __getitem__(self, index: int) -> Processor:
        with self._lock:
            return self._processors[index]

    def __contains__(self, processor: Processor) -> bool:
        with self._lock:
            return processor in self._processors

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(processors_count={len(self._processors)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(processors={self._processors})"
