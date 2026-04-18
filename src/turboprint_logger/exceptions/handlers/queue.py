from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException

__all__ = (
    "QueueHandlerClosedError",
    "QueueHandlerException",
)


class QueueHandlerException(HandlerException):
    """Base exception for queue handler errors."""


class QueueHandlerClosedError(QueueHandlerException):
    """Raised when attempting to use a closed queue handler."""
