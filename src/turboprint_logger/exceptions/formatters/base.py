from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("FormatterException",)


class FormatterException(TurboPrintException):
    """Base exception for all formatters exceptions"""
