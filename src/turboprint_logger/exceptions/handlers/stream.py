from __future__ import annotations

from turboprint_logger.exceptions.handlers.base import HandlerException

__all__ = (
    "InvalidBufferSizeError",
    "InvalidStreamError",
    "InvalidStreamFlushIntervalError",
    "StreamHandlerException",
)


class StreamHandlerException(HandlerException):
    """Base exception for stream handler errors."""


class InvalidStreamError(StreamHandlerException):
    """Raised when stream object does not support required operations."""


class InvalidBufferSizeError(StreamHandlerException):
    """Raised when buffered stream handler buffer size is invalid."""


class InvalidStreamFlushIntervalError(StreamHandlerException):
    """Raised when buffered stream handler flush interval is invalid."""
