from __future__ import annotations

from turboprint_logger.exceptions.core.base import CoreException

__all__ = (
    "PluginAlreadyRegisteredError",
    "PluginException",
    "PluginNotFoundError",
    "PluginTypeError",
)


class PluginException(CoreException):
    """Base exception for all plugins exceptions"""


class PluginNotFoundError(PluginException):
    """Raised when a plugin is not found"""


class PluginAlreadyRegisteredError(PluginException):
    """Raised when a plugin is already registered"""


class PluginTypeError(PluginException):
    """Raised when a plugin is not the correct type"""
