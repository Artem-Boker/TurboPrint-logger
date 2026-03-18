from __future__ import annotations


class LoggerException(Exception):
    """Base exception for logger-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class LoggerInstantiationError(LoggerException):
    """Raised when attempting to instantiate a Logger directly."""
