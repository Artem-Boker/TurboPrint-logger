from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class CollectionsError(ManagerException):
    """Raised when a collections manager encounters an error."""
