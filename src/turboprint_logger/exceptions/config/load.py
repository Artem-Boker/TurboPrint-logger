from __future__ import annotations

from turboprint_logger.exceptions.config.base import ConfigException


class LoadConfigException(ConfigException):
    """Exception raised when the config cannot be loaded."""
