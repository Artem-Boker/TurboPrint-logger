from __future__ import annotations


class ContainerException(Exception):
    """Base exception for all container exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContainerInstantiationError(ContainerException):
    """Raised when attempting to instantiate a Container directly."""


class ContainerNotFoundError(ContainerException):
    """Raised when a container with given name does not exist."""
