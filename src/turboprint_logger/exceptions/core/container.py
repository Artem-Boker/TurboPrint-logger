from __future__ import annotations

from turboprint_logger.exceptions.core.base import CoreException

__all__ = ("ContainerException", "ContainerInstantiationError")


class ContainerException(CoreException):
    """Base exception for all container exceptions"""


class ContainerInstantiationError(ContainerException):
    """Exception raised when container cannot be instantiated"""
