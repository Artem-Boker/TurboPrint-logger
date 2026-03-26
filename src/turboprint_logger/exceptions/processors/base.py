from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("ProcessorException",)


class ProcessorException(TurboPrintException):
    """Base exception for all processors exceptions"""
