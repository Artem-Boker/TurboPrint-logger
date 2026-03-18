from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class ConfigManagerError(ManagerException):
    """Raised when a config manager encounters an error."""
