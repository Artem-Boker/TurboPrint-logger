from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class ContextManagerError(ManagerException):
    """Raised when a context manager encounters an error."""
