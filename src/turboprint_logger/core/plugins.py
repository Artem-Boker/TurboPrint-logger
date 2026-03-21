from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import TypeVar

from turboprint_logger.exceptions.core.plugins import (
    PluginAlreadyRegisteredError,
    PluginNotFoundError,
    PluginTypeError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler

_T = TypeVar("_T", bound=type[Handler | Filter | Formatter])
_HANDLER = TypeVar("_HANDLER", bound=type[Handler])
_FILTER = TypeVar("_FILTER", bound=type[Filter])
_FORMATTER = TypeVar("_FORMATTER", bound=type[Formatter])

_handlers_lock = RLock()
_filters_lock = RLock()
_formatters_lock = RLock()

_handlers: dict[str, type[Handler]] = {}
_filters: dict[str, type[Filter]] = {}
_formatters: dict[str, type[Formatter]] = {}


def _register(
    type_: _T, lock: RLock, dict_: dict[str, _T], name: str | None = None
) -> Callable[[_T], _T]:
    def decorator(cls: _T) -> _T:
        if not issubclass(cls, type_):
            msg = f"{cls.__name__} mist be subclass of {type_.__name__}"
            raise PluginTypeError(msg)
        with lock:
            key = name or cls.__name__
            if key in dict_ and dict_[key] is not cls:
                msg = f"{cls.__name__} {key!r} already registered"
                raise PluginAlreadyRegisteredError(msg)
            dict_[key] = cls
        return cls

    return decorator


def _get(dict_: dict[str, _T], type_: _T, name: str) -> _T:
    try:
        return dict_[name]
    except KeyError:
        msg = f"Unknown {type_.__name__.lower()}: {name}"
        raise PluginNotFoundError(msg) from None


def register_handler(name: str | None = None) -> Callable[[_HANDLER], _HANDLER]:
    return _register(Handler, _handlers_lock, _handlers, name)  # pyright: ignore[reportReturnType]


def get_handler(name: str) -> type[Handler]:
    return _get(_handlers, Handler, name)


def register_filter(name: str | None = None) -> Callable[[_FILTER], _FILTER]:
    return _register(Filter, _filters_lock, _filters, name)  # pyright: ignore[reportReturnType]


def get_filter(name: str) -> type[Filter]:
    return _get(_filters, Filter, name)


def register_formatter(name: str | None = None) -> Callable[[_FORMATTER], _FORMATTER]:
    return _register(Formatter, _formatters_lock, _formatters, name)  # pyright: ignore[reportReturnType]


def get_formatter(name: str) -> type[Formatter]:
    return _get(_formatters, Formatter, name)
