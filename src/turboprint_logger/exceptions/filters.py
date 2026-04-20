from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("FilterException",)


class FilterException(TurboPrintException):
    """Base exception for all filters exceptions"""


class NameFilterException(FilterException):
    """Base exception for all name filter exceptions"""


class InvalidFilterModeError(NameFilterException):
    """Raised when the filter mode is invalid"""


class RateLimitFilterException(FilterException):
    "Base exception for all rate limit filter exceptions"


class InvalidRateLimitError(RateLimitFilterException):
    "Raised when the rate limit is invalid"
