from __future__ import annotations

from functools import lru_cache
from re import IGNORECASE
from re import fullmatch as re_full
from re import search as re_search

from turboprint_logger.exceptions.utils.normalizers import (
    InvalidContainerNameError,
    InvalidContextKeyError,
    InvalidLevelNameError,
    InvalidLoggerNameError,
)


@lru_cache(maxsize=1024)
def _normalize(name: str, pattern: str, *, upper: bool = True) -> str | None:
    name = name.strip().upper() if upper else name.strip().lower()
    if not re_full(pattern, name, IGNORECASE):
        return None
    if re_search(r"^[_.-]|[_.-]$", name, IGNORECASE):
        return None
    if re_search(r"\.\.|--|__", name, IGNORECASE):
        return None
    return name


def normalize_container_name(name: str) -> str:
    normal_name = _normalize(name, r"[a-z0-9_-]+", upper=False)
    if not normal_name:
        msg = f"Invalid container name: {name}"
        raise InvalidContainerNameError(msg)
    return normal_name


def normalize_logger_name(name: str) -> str:
    normal_name = _normalize(name, r"[a-z0-9_.-]+", upper=False)
    if not normal_name:
        msg = f"Invalid logger name: {name}"
        raise InvalidLoggerNameError(msg)
    return normal_name


def normalize_level_name(name: str) -> str:
    normal_name = _normalize(name, r"[a-z_-]+", upper=True)
    if not normal_name:
        msg = f"Invalid level name: {name}"
        raise InvalidLevelNameError(msg)
    return normal_name


def normalize_context_key(key: str) -> str:
    normal_name = _normalize(key, r"[a-z0-9_-]+", upper=False)
    if not normal_name:
        msg = f"Invalid context key: {key}"
        raise InvalidContextKeyError(msg)
    return normal_name
