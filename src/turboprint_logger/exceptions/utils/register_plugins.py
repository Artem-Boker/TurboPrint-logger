from __future__ import annotations

from turboprint_logger.exceptions.utils.base import ValidationException


class PluginRegistrationError(ValidationException):
    """Raised when a plugin registration encounters an error."""
