from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class RegexFilterError(FilterException):
    """Raised when a regex filter encounters an error."""
