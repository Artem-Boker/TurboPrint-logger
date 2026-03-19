from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class MetricsException(ManagerException):
    """Base exception for all metrics managers exceptions"""


class NegativeMetricsCountError(MetricsException):
    """Raised when the metrics count is negative"""
