from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class ConfigManagerException(ManagerException):
    """Base exception for ConfigManager errors"""


class ConfigParserError(ConfigManagerException):
    """Raised when config parsing fails"""


class ConfigSpecError(ConfigManagerException):
    """Raised when config schema/values are invalid"""


class ConfigReloadError(ConfigManagerException):
    """Raised for auto-reload runtime errors"""


class ConfigWatchAlreadyRunningError(ConfigReloadError):
    """Raised when auto-reload is enabled twice"""
