from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class StatusManagerError(ManagerException):
    """Raised when a status manager encounters an error."""
