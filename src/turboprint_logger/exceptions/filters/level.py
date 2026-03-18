from __future__ import annotations

from turboprint_logger.exceptions.filters.base import FilterException


class LevelFilterError(FilterException):
    """Raised when a level filter encounters an error."""
