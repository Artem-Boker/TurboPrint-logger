from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException

__all__ = (
    "FileClosedError",
    "FileHandlerConfigError",
    "FileHandlerException",
    "FileOpenError",
    "FileWriteError",
    "InvalidFlushIntervalError",
    "InvalidSeparatorError",
)


class FileHandlerException(HandlerException):
    """Base exception for all file handlers exceptions"""


class FileClosedError(FileHandlerException):
    """Raised when the file is closed"""


class FileHandlerConfigError(FileHandlerException):
    """Raised when file handler configuration is invalid."""


class InvalidSeparatorError(FileHandlerConfigError):
    """Raised when separator is not a non-empty string."""


class InvalidFlushIntervalError(FileHandlerConfigError):
    """Raised when flush interval is invalid."""


class FileOpenError(FileHandlerException):
    """Raised when the file cannot be opened"""


class FileWriteError(FileHandlerException):
    """Raised when the file cannot be written"""
