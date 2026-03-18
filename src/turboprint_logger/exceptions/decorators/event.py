from __future__ import annotations


class EventException(Exception):
    """Base exception for event-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
