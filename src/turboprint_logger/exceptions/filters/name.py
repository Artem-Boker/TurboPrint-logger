from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class NameFilterException(FilterException):
    """Base exception for all name filter exceptions"""


class InvalidFilterModeError(NameFilterException):
    """Raised when the filter mode is invalid"""
