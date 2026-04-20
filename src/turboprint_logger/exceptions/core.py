from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("CoreException",)


class CoreException(TurboPrintException):
    """Base exception for all core exceptions"""


class ContainerException(CoreException):
    """Base exception for all container exceptions"""


class ContainerInstantiationError(ContainerException):
    """Exception raised when container cannot be instantiated"""


class LevelException(CoreException):
    """Base exception for all levels exceptions"""


class InvalidLevelColorError(LevelException):
    """Raised when the level color is invalid"""


class InvalidLevelEmojiError(LevelException):
    """Raised when the level emoji is invalid"""


class LevelNameAlreadyExistsError(LevelException):
    """Raised when the level name already exists"""


class LevelValueAlreadyExistsError(LevelException):
    """Raised when the level value already exists"""


class NegativeLevelError(LevelException):
    """Raised when the level value is negative"""


class LoggerException(CoreException):
    """Base exception for all loggers exceptions"""


class LoggerInstantiationError(LoggerException):
    """Exception raised when logger cannot be instantiated"""


class PluginException(CoreException):
    """Base exception for all plugins exceptions"""


class PluginNotFoundError(PluginException):
    """Raised when a plugin is not found"""


class PluginAlreadyRegisteredError(PluginException):
    """Raised when a plugin is already registered"""


class PluginTypeError(PluginException):
    """Raised when a plugin is not the correct type"""
