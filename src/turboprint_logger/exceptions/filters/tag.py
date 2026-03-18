from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class TagFilterError(FilterException):
    """Raised when a tag filter encounters an error."""
