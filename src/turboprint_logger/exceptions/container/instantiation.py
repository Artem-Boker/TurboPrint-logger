from __future__ import annotations

from turboprint_logger.exceptions.container.base import ContainerException


class ContainerInstantiationError(ContainerException):
    """Raised when attempting to instantiate a Container directly."""
