from __future__ import annotations


class ConfigException(Exception):
    """Base exception for all config exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
