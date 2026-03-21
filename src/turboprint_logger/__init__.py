from __future__ import annotations

from .core import Config, Container, Level, Logger, get_default_container
from .integrations.logging import LoggingAdapter
from .managers import ConfigManager, LocaleManager

get_logger = Logger.get_logger
get_container = Container.get_container

__all__ = [
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
]

__version__ = "0.2.1"
