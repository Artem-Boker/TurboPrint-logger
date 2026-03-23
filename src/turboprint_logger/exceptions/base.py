from __future__ import annotations

__all__ = ("TurboPrintException",)


class TurboPrintException(Exception):
    """Base exception for all TurboPrint exceptions"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
