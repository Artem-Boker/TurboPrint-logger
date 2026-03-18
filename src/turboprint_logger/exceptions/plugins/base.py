from __future__ import annotations


class PluginException(Exception):
    """Base exception for all plugin exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class PluginTypeError(PluginException):
    """Raised when a plugin is not a subclass of required type."""


class PluginAlreadyRegisteredError(PluginException):
    """Raised when a plugin with the same name is already registered."""


class PluginNotFoundError(PluginException):
    """Raised when a plugin with given name is not found."""
