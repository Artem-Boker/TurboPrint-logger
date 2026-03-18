from __future__ import annotations

from turboprint_logger.exceptions.container.base import ContainerException


class ContainerNotFoundError(ContainerException):
    """Raised when a container with given name does not exist."""
