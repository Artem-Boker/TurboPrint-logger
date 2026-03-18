from __future__ import annotations


class TimedException(Exception):
    """Base exception for timed-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
