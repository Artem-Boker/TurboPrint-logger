from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("DecoratorException",)


class DecoratorException(TurboPrintException):
    """Base exception for all decorators exceptions"""
