from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException


class StreamHandlerError(HandlerException):
    """Raised when a stream handler encounters an error."""
