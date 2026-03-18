from __future__ import annotations

from turboprint_logger.exceptions.managers.base import ManagerException


class MetricsError(ManagerException):
    """Base exception for metrics-related errors."""


class NegativeMetricsCountError(MetricsError):
    """Raised when attempting to set a negative count for metrics."""
