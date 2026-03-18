from __future__ import annotations


class ManagerException(Exception):
    """Base exception for manager-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class MetricsError(ManagerException):
    """Base exception for metrics-related errors."""


class NegativeMetricsCountError(MetricsError):
    """Raised when attempting to set a negative count for metrics."""
