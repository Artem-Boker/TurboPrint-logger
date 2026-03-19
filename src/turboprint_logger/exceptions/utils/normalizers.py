from __future__ import annotations

from turboprint_logger.exceptions.utils.base import UtilException


class NormalizerException(UtilException):
    """Base exception for all normalizers utils exceptions"""


class InvalidContainerNameError(NormalizerException):
    """Raised when the container name is invalid"""


class InvalidContextKeyError(NormalizerException):
    """Raised when the context key is invalid"""


class InvalidLevelNameError(NormalizerException):
    """Raised when the level name is invalid"""


class InvalidLoggerNameError(NormalizerException):
    """Raised when the logger name is invalid"""
