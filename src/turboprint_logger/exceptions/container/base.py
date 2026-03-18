from __future__ import annotations


class ContainerException(Exception):
    """Base exception for all container exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
