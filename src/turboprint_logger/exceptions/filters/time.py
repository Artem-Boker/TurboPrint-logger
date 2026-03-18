from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class TimeFilterError(FilterException):
    """Raised when a time filter encounters an error."""
