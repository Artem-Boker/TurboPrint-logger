from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("ManagerException",)


class ManagerException(TurboPrintException):
    """Base exception for all managers exceptions"""


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


class MetricsException(ManagerException):
    """Base exception for all metrics managers exceptions"""


class NegativeMetricsCountError(MetricsException):
    """Raised when the metrics count is negative"""
