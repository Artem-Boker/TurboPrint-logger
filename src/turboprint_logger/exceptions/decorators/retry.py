from __future__ import annotations


class RetryException(Exception):
    """Base exception for retry-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class RetryError(RetryException):
    """Raised when an unknown error occurs in retry."""
