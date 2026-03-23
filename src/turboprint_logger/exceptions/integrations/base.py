from __future__ import annotations

from turboprint_logger.exceptions.base import TurboPrintException

__all__ = ("IntegrationException",)


class IntegrationException(TurboPrintException):
    """Base exception for all integrations exceptions"""
