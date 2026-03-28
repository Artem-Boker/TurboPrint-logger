from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = (
    "InterfaceException",
    "InterfaceMethodNotImplementedError",
)


class InterfaceException(TurboPrintException):
    """Base exception for interface contract errors."""


class InterfaceMethodNotImplementedError(InterfaceException):
    """Raised when an interface method is not implemented by a subclass."""
