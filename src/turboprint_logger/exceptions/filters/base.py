from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("FilterException",)


class FilterException(TurboPrintException):
    """Base exception for all filters exceptions"""
