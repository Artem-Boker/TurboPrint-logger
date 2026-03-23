from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("CoreException",)


class CoreException(TurboPrintException):
    """Base exception for all core exceptions"""
