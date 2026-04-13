from __future__ import annotations

import re

from turboprint_logger.exceptions.utils.normalizers import (
    InvalidContainerNameError,
    InvalidContextKeyError,
    InvalidLevelNameError,
    InvalidLoggerNameError,
)

__all__ = (
    "normalize_container_name",
    "normalize_context_key",
    "normalize_level_name",
    "normalize_logger_name",
)

_PATTERN_CONTAINER = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)
_PATTERN_LOGGER = re.compile(r"[a-z0-9_.-]+", re.IGNORECASE)
_PATTERN_LEVEL = re.compile(r"[a-z_-]+", re.IGNORECASE)
_PATTERN_CONTEXT = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)

_BAD_BOUNDARIES = re.compile(r"^[_.-]|[_.-]$", re.IGNORECASE)
_BAD_DOUBLE = re.compile(r"[_.-]+", re.IGNORECASE)


def _normalize(name: str, pattern: re.Pattern, *, upper: bool = True) -> str | None:
    name = name.strip().upper() if upper else name.strip().lower()
    if not pattern.fullmatch(name):
        return None
    if _BAD_BOUNDARIES.search(name):
        return None
    if _BAD_DOUBLE.search(name):
        return None
    return name


def normalize_container_name(name: str) -> str:
    normal_name = _normalize(name, _PATTERN_CONTAINER, upper=False)
    if not normal_name:
        msg = f"Invalid container name: {name}"
        raise InvalidContainerNameError(msg)
    return normal_name


def normalize_logger_name(name: str) -> str:
    normal_name = _normalize(name, _PATTERN_LOGGER, upper=False)
    if not normal_name:
        msg = f"Invalid logger name: {name}"
        raise InvalidLoggerNameError(msg)
    return normal_name


def normalize_level_name(name: str) -> str:
    normal_name = _normalize(name, _PATTERN_LEVEL, upper=True)
    if not normal_name:
        msg = f"Invalid level name: {name}"
        raise InvalidLevelNameError(msg)
    return normal_name


def normalize_context_key(key: str) -> str:
    normal_name = _normalize(key, _PATTERN_CONTEXT, upper=False)
    if not normal_name:
        msg = f"Invalid context key: {key}"
        raise InvalidContextKeyError(msg)
    return normal_name
