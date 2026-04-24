from __future__ import annotations

from contextlib import contextmanager
from threading import Lock, RLock, local
from typing import Generic, TypeVar

from turboprint_logger.utils.normalizers import normalize_context_key

__all__ = ("TemporaryMixin",)
T = TypeVar("T")
_MISSING = object()


class TemporaryMixin(Generic[T]):
    _lock: Lock | RLock
    _thread_local: local

    @contextmanager
    def temporary(  # noqa: ANN202, C901, PLR0912, PLR0915
        self,
        *args,
        replace: bool = True,
        **kwargs,
    ):
        if not hasattr(self._thread_local, "stack"):
            self._thread_local.stack = []

        with self._lock:
            if hasattr(self, "_enabled"):
                if args:
                    msg = "Status temporary() accepts only keyword arguments."
                    raise TypeError(msg)
                unknown = set(kwargs) - {"status"}
                if unknown:
                    names = ", ".join(sorted(unknown))
                    msg = f"Unexpected keyword argument(s): {names}"
                    raise TypeError(msg)
                status = kwargs.pop("status", True)
                self._thread_local.stack.append(self._enabled)
                self._enabled = status
            elif hasattr(self, "_item"):
                item = kwargs.pop("item", _MISSING)
                if item is not _MISSING and args:
                    msg = (
                        "Item temporary() accepts either positional or keyword `item`."
                    )
                    raise TypeError(msg)
                if item is _MISSING:
                    if len(args) != 1:
                        msg = "Item temporary() accepts exactly one positional item."
                        raise TypeError(msg)
                    item = args[0]
                if kwargs:
                    msg = "Item temporary() accepts only `item`."
                    raise TypeError(msg)
                self._thread_local.stack.append(self._item)
                self._item = item
            elif hasattr(self, "_items") and isinstance(self._items, list):
                if kwargs:
                    msg = "Collection temporary() accepts only positional items."
                    raise TypeError(msg)
                self._thread_local.stack.append(self._items.copy())
                self._items = list(args) if replace else [*self._items, *args]
            elif hasattr(self, "_items") and isinstance(self._items, dict):
                items = kwargs
                if args:
                    msg = "Context temporary() accepts only keyword items."
                    raise TypeError(msg)
                normalized = {
                    normalize_context_key(key): value for key, value in items.items()
                }
                self._thread_local.stack.append(self._items.copy())
                self._items = normalized if replace else {**self._items, **normalized}
            else:
                msg = f"{self.__class__.__name__} does not support temporary override."
                raise TypeError(msg)

            try:
                yield
            finally:
                if hasattr(self, "_enabled"):
                    self._enabled = self._thread_local.stack.pop()
                elif hasattr(self, "_item"):
                    self._item = self._thread_local.stack.pop()
                else:
                    self._items = self._thread_local.stack.pop()
