from __future__ import annotations


class DeprecatedException(Exception):
    """Base exception for deprecated-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
