from __future__ import annotations

import re

from turboprint_logger.exceptions.utils import (
    InvalidContainerNameError,
    InvalidContextKeyError,
    InvalidLevelNameError,
    InvalidLoggerNameError,
    NormalizerException,
)

__all__ = (
    "normalize_container_name",
    "normalize_context_key",
    "normalize_level_name",
    "normalize_logger_name",
)

_PATTERN_CONTAINER = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)
_PATTERN_LOGGER = re.compile(r"[a-z0-9_.-]+", re.IGNORECASE)
_PATTERN_LEVEL = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)
_PATTERN_CONTEXT = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)

_BAD_BOUNDARIES = re.compile(r"^[_.-]|[_.-]$", re.IGNORECASE)
_BAD_DOUBLE = re.compile(r"[_.-]{2,}", re.IGNORECASE)


def _normalize(
    error_message: str,
    exception_type: type[NormalizerException],
    name: str,
    pattern: re.Pattern,
    *,
    upper: bool = True,
) -> str:
    name = name.strip().upper() if upper else name.strip().lower()
    returned = True
    if not name:
        returned = False
    if not pattern.fullmatch(name):
        returned = False
    if _BAD_BOUNDARIES.search(name):
        returned = False
    if _BAD_DOUBLE.search(name):
        returned = False

    if returned:
        return name

    msg = f"Invalid {error_message}: {name}"
    raise exception_type(msg)


def normalize_container_name(name: str) -> str:
    return _normalize(
        "container name",
        InvalidContainerNameError,
        name,
        _PATTERN_CONTAINER,
        upper=False,
    )


def normalize_logger_name(name: str) -> str:
    return _normalize(
        "logger name", InvalidLoggerNameError, name, _PATTERN_LOGGER, upper=False
    )


def normalize_level_name(name: str) -> str:
    return _normalize(
        "level name", InvalidLevelNameError, name, _PATTERN_LEVEL, upper=True
    )


def normalize_context_key(key: str) -> str:
    return _normalize(
        "context key", InvalidContextKeyError, key, _PATTERN_CONTEXT, upper=False
    )
