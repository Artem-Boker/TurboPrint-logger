from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException


class FileHandlerError(HandlerException, OSError):
    """Base exception for file handler errors."""


class FileOpenError(FileHandlerError):
    """Raised when a file cannot be opened."""


class FileClosedError(FileHandlerError):
    """Raised when attempting to write to a closed file."""
