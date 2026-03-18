from __future__ import annotations


class BaseConfigException(Exception):
    """Base exception for all config exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidConfigException(BaseConfigException):
    """Exception raised when the config is invalid."""


class LoadConfigException(BaseConfigException):
    """Exception raised when the config cannot be loaded."""


class SaveConfigException(BaseConfigException):
    """Exception raised when the config cannot be saved."""
