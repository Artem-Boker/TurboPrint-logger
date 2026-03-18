from __future__ import annotations


class CoreException(Exception):
    """Base exception for all core exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContainerException(CoreException):
    """Base exception for container-related errors."""


class LoggerException(CoreException):
    """Base exception for logger-related errors."""


class LevelException(CoreException):
    """Base exception for level-related errors."""


class PluginException(CoreException):
    """Base exception for plugin-related errors."""