from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class HandlersManagerError(ManagerException):
    """Raised when a handlers manager encounters an error."""
