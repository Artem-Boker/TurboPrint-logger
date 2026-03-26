from __future__ import annotations

from contextlib import contextmanager
from threading import RLock

__all__ = ("StatusManager",)


class StatusComponent:
    __slots__ = ("_lock", "enabled")

    def __init__(self, *, status: bool = True) -> None:
        self._lock = RLock()
        self.enabled = status

    def get(self) -> bool:
        with self._lock:
            return self.enabled

    def set(self, status: bool) -> None:  # noqa: FBT001
        with self._lock:
            self.enabled = status

    def toggle(self) -> bool:
        with self._lock:
            self.enabled = not self.enabled
            return self.enabled

    def enable(self) -> None:
        with self._lock:
            self.enabled = True

    def disable(self) -> None:
        with self._lock:
            self.enabled = False

    @contextmanager
    def temporary(self, *, status: bool = True):  # noqa: ANN202
        with self._lock:
            original = self.enabled
            self.enabled = status
            try:
                yield
            finally:
                self.enabled = original

    def __bool__(self) -> bool:
        with self._lock:
            return self.enabled

    def __str__(self) -> str:
        return str(self.enabled)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status={self.enabled})"


class StatusManager:
    __slots__ = ("filters", "global_filters", "global_handlers", "handlers", "logger")

    def __init__(
        self,
        *,
        logger: bool = True,
        handlers: bool = True,
        filters: bool = True,
        global_handlers: bool = True,
        global_filters: bool = True,
    ) -> None:
        self.logger = StatusComponent(status=logger)
        self.handlers = StatusComponent(status=handlers)
        self.filters = StatusComponent(status=filters)
        self.global_handlers = StatusComponent(status=global_handlers)
        self.global_filters = StatusComponent(status=global_filters)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(logger_enabled={self.logger.enabled})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"logger={self.logger}, "
            f"handlers={self.handlers}, "
            f"filters={self.filters}, "
            f"global_handlers={self.global_handlers}, "
            f"global_filters={self.global_filters})"
        )
