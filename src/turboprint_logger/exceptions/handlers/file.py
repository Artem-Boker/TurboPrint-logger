from __future__ import annotations


class HandlerException(Exception):
    """Base exception for handler-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FileHandlerError(HandlerException, OSError):
    """Base exception for file handler errors."""


class FileOpenError(FileHandlerError):
    """Raised when a file cannot be opened."""


class FileClosedError(FileHandlerError):
    """Raised when attempting to write to a closed file."""
