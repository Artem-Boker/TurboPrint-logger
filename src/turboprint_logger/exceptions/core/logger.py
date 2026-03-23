from __future__ import annotations

from turboprint_logger.exceptions.core.base import CoreException

__all__ = ("LoggerException", "LoggerInstantiationError")


class LoggerException(CoreException):
    """Base exception for all loggers exceptions"""


class LoggerInstantiationError(LoggerException):
    """Exception raised when logger cannot be instantiated"""
