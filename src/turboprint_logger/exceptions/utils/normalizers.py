from __future__ import annotations

from turboprint_logger.exceptions.utils.base import ValidationException


class NormalizationError(ValidationException):
    """Base exception for normalization errors."""


class InvalidContainerNameError(NormalizationError):
    """Raised when a container name is invalid."""


class InvalidLoggerNameError(NormalizationError):
    """Raised when a logger name is invalid."""


class InvalidLevelNameError(NormalizationError):
    """Raised when a level name is invalid."""


class InvalidContextKeyError(NormalizationError):
    """Raised when a context key is invalid."""
