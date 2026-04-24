from __future__ import annotations

from threading import RLock, local

from turboprint_logger.managers._mixins import TemporaryMixin

__all__ = ("StatusManager",)


class StatusComponent(TemporaryMixin[bool]):
    __slots__ = ("_enabled", "_lock", "_thread_local")

    def __init__(self, *, status: bool = True) -> None:
        self._lock = RLock()
        self._enabled = status
        self._thread_local = local()

    @property
    def enabled(self) -> bool:
        return self.get()

    def get(self) -> bool:
        with self._lock:
            return self._enabled

    def set(self, status: bool) -> None:  # noqa: FBT001
        with self._lock:
            self._enabled = status

    def toggle(self) -> bool:
        with self._lock:
            self._enabled = not self._enabled
            return self._enabled

    def enable(self) -> None:
        with self._lock:
            self._enabled = True

    def disable(self) -> None:
        with self._lock:
            self._enabled = False

    def __bool__(self) -> bool:
        with self._lock:
            return self._enabled

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
        return f"{self.__class__.__name__}({self.logger.enabled})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"logger={self.logger}, "
            f"handlers={self.handlers}, "
            f"filters={self.filters}, "
            f"global_handlers={self.global_handlers}, "
            f"global_filters={self.global_filters})"
        )
