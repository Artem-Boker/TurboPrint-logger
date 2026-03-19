from __future__ import annotations

from turboprint_logger.exceptions.core.base import CoreException


class LevelException(CoreException):
    """Base exception for all levels exceptions"""


class InvalidLevelColorError(LevelException):
    """Raised when the level color is invalid"""


class InvalidLevelEmojiError(LevelException):
    """Raised when the level emoji is invalid"""


class LevelNameAlreadyExistsError(LevelException):
    """Raised when the level name already exists"""


class LevelValueAlreadyExistsError(LevelException):
    """Raised when the level value already exists"""


class NegativeLevelError(LevelException):
    """Raised when the level value is negative"""
