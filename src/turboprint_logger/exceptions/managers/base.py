from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("ManagerException",)


class ManagerException(TurboPrintException):
    """Base exception for all managers exceptions"""
