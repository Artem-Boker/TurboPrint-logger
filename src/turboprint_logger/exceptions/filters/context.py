from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class ContextFilterError(FilterException):
    """Raised when a context filter encounters an error."""
