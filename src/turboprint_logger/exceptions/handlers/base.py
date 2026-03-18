from __future__ import annotations


class HandlerException(Exception):
    """Base exception for handler-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
