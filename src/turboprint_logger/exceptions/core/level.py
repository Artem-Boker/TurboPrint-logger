from __future__ import annotations

from turboprint_logger.exceptions.core.base import LevelException


class LevelRegistrationError(LevelException):
    """Base exception for level registration errors."""


class LevelNameAlreadyExistsError(LevelRegistrationError):
    """Raised when a level with the same name already exists."""


class LevelValueAlreadyExistsError(LevelRegistrationError):
    """Raised when a level with the same value already exists."""


class NegativeLevelError(LevelRegistrationError):
    """Raised when a level value is negative."""


class InvalidLevelColorError(LevelRegistrationError):
    """Raised when a level color is invalid."""


class InvalidLevelEmojiError(LevelRegistrationError):
    """Raised when a level emoji is invalid."""
