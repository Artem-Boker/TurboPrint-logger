from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("UtilException",)


class UtilException(TurboPrintException):
    """Base exception for all utils exceptions"""
