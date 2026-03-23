from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("HandlerException",)


class HandlerException(TurboPrintException):
    """Base exception for all handlers exceptions"""
