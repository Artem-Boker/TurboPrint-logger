from __future__ import annotations

from . import filters, formatters, handlers, processors
from .core import (
    Config,
    Container,
    Level,
    LevelRegistry,
    Record,
    Logger,
    get_default_container,
)
from .core import plugins as __plugins
from .integrations.logging import LoggingAdapter
from .managers import ConfigManager, LocaleManager

get_logger = Logger.get_logger
get_container = Container.get_container

__all__ = (
    "Config",
    "ConfigManager",
    "Container",
    "Level",
    "LocaleManager",
    "Logger",
    "LoggingAdapter",
    "get_container",
    "get_default_container",
    "get_logger",
    "LevelRegistry",
    "Record",
)

__version__ = "0.2.6"


def __register_from_package(package, registry_func) -> None:  # noqa: ANN001
    if not hasattr(package, "__all__"):
        return
    for name in package.__all__:
        cls = getattr(package, name)
        registry_func(name)(cls)


__register_from_package(filters, __plugins.register_filter)
__register_from_package(formatters, __plugins.register_formatter)
__register_from_package(handlers, __plugins.register_handler)
__register_from_package(processors, __plugins.register_processor)
