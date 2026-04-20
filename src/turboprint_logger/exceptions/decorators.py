from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("DecoratorException",)


class DecoratorException(TurboPrintException):
    """Base exception for all decorators exceptions"""


class RetryException(DecoratorException):
    """Base exception for all retry decorator exceptions"""


class RetryLimitExceededError(RetryException):
    """Raised when the retry limit is exceeded"""


class UnknownRetryError(RetryException):
    """Raised when an unknown error occurs"""
