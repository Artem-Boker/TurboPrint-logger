from __future__ import annotations


class TurboPrintException(Exception):
    """Base exception for all TurboPrint exceptions"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
