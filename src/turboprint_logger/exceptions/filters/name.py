from __future__ import annotations


class FilterException(Exception):
    """Base exception for filter-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidFilterModeError(FilterException):
    """Raised when an invalid filter mode is provided."""
