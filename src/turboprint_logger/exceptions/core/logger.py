from __future__ import annotations

from turboprint_logger.exceptions.core.base import LoggerException


class LoggerInstantiationError(LoggerException):
    """Raised when attempting to instantiate a Logger directly."""
