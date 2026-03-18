from __future__ import annotations


class ValidationException(Exception):
    """Base exception for validation errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
