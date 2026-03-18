from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class FormatterManagerError(ManagerException):
    """Raised when a formatter manager encounters an error."""
