from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class CompositeFilterError(FilterException):
    """Raised when a composite filter encounters an error."""
