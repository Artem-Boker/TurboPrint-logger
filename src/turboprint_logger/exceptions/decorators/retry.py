from __future__ import annotations

from turboprint_logger.exceptions.decorators.base import DecoratorException


class RetryException(DecoratorException):
    """Base exception for all retry decorator exceptions"""


class RetryLimitExceededError(RetryException):
    """Raised when the retry limit is exceeded"""


class UnknownRetryError(RetryException):
    """Raised when an unknown error occurs"""
