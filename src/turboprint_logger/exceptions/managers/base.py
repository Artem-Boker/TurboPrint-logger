from __future__ import annotations


class ManagerException(Exception):
    """Base exception for manager-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
