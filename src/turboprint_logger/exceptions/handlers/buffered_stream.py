from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException


class BufferedStreamHandlerError(HandlerException):
    """Raised when a buffered stream handler encounters an error."""
