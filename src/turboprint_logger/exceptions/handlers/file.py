from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException

__all__ = (
    "FileClosedError",
    "FileHandlerException",
    "FileOpenError",
    "FileWriteError",
)


class FileHandlerException(HandlerException):
    """Base exception for all file handlers exceptions"""


class FileClosedError(FileHandlerException):
    """Raised when the file is closed"""


class FileOpenError(FileHandlerException):
    """Raised when the file cannot be opened"""


class FileWriteError(FileHandlerException):
    """Raised when the file cannot be written"""
