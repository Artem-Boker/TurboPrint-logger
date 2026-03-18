from __future__ import annotations

from .core import Config, Container, Level, Logger, get_default_container
from .integrations.logging import LoggingAdapter
from .managers import LocaleManager

get_logger = Logger.get_logger

__all__ = [
    "Config",
    "Container",
    "Level",
    "LocaleManager",
    "Logger",
    "LoggingAdapter",
    "get_default_container",
    "get_logger",
]

__version__ = "0.1.0"
