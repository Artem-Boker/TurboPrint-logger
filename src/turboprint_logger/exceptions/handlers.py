from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("HandlerException",)


class HandlerException(TurboPrintException):
    """Base exception for all handlers exceptions"""


class CloseException(HandlerException):
    """Raised when the handler cannot be closed"""


class FileHandlerException(HandlerException):
    """Base exception for all file handlers exceptions"""


class FileClosedError(FileHandlerException):
    """Raised when the file is closed"""


class FileHandlerConfigError(FileHandlerException):
    """Raised when file handler configuration is invalid."""


class InvalidSeparatorError(FileHandlerConfigError):
    """Raised when separator is not a non-empty string."""


class InvalidFlushIntervalError(FileHandlerConfigError):
    """Raised when flush interval is invalid."""


class FileOpenError(FileHandlerException):
    """Raised when the file cannot be opened"""


class FileWriteError(FileHandlerException):
    """Raised when the file cannot be written"""


class QueueHandlerException(HandlerException):
    """Base exception for queue handler errors."""


class QueueHandlerClosedError(QueueHandlerException):
    """Raised when attempting to use a closed queue handler."""


class RotatingFileHandlerException(HandlerException):
    "Base exception for all rotating file handler exceptions"


class InvalidWhenValueRotatingFileHandlerError(RotatingFileHandlerException):
    "Raised when the rotating file handler is invalid"


class StreamHandlerException(HandlerException):
    """Base exception for stream handler errors."""


class InvalidStreamError(StreamHandlerException):
    """Raised when stream object does not support required operations."""


class InvalidBufferSizeError(StreamHandlerException):
    """Raised when buffered stream handler buffer size is invalid."""


class InvalidStreamFlushIntervalError(StreamHandlerException):
    """Raised when buffered stream handler flush interval is invalid."""
