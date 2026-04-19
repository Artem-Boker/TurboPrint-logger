from __future__ import annotations

from contextlib import contextmanager
from threading import RLock, local

from turboprint_logger.formatters import SimpleFormatter
from turboprint_logger.interfaces import Formatter

__all__ = ("FormatterManager",)


class FormatterManager:
    __slots__ = ("_formatter", "_lock", "_thread_local")

    def __init__(self, formatter: Formatter | None = None) -> None:
        self._lock = RLock()
        self._formatter = formatter or SimpleFormatter()
        self._thread_local = local()

    def get(self) -> Formatter:
        with self._lock:
            return self._formatter

    def set(self, formatter: Formatter) -> None:
        with self._lock:
            self._formatter = formatter

    @contextmanager
    def temporary(self, formatter: Formatter):  # noqa: ANN201
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            snapshot = self._formatter
            self._thread_local.stack.append(snapshot)
            self._formatter = formatter

            try:
                yield
            finally:
                self._formatter = self._thread_local.stack.pop()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(formatter={self._formatter})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(formatter={self._formatter!r})"
