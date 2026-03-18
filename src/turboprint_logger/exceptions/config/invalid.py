from __future__ import annotations

from turboprint_logger.exceptions.config.base import ConfigException


class InvalidConfigException(ConfigException):
    """Exception raised when the config is invalid."""


class InvalidConfigValueException(InvalidConfigException):
    """Exception raised when the config value is invalid."""


class InvalidConfigKeyException(InvalidConfigException):
    """Exception raised when the config key is invalid."""


class InvalidConfigTypeException(InvalidConfigException):
    """Exception raised when the config type is invalid."""


class InvalidConfigSectionException(InvalidConfigException):
    """Exception raised when the config section is invalid."""
