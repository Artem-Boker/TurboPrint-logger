from __future__ import annotations

from turboprint_logger.exceptions.config.base import ConfigException


class SaveConfigException(ConfigException):
    """Exception raised when the config cannot be saved."""
