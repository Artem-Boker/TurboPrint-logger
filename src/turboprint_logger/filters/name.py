from __future__ import annotations

from re import IGNORECASE
from re import compile as re_compile
from typing import Literal, get_args

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

_MODES = Literal["exact", "startswith", "endswith", "contains", "regex"]


class NameFilter(Filter):
    def __init__(self, pattern: str, mode: _MODES, *, ignorecase: bool = True) -> None:
        if mode.lower() not in get_args(_MODES):
            msg = f"Invalid mode: {mode.lower()}"
            raise ValueError(msg)

        self.pattern = pattern
        self.mode = mode.lower()
        self.ignorecase = ignorecase

        if mode == "regex":
            flags = IGNORECASE if ignorecase else 0
            self._regex = re_compile(pattern, flags)

    def filter(self, record: Record) -> bool:
        name = record.logger.name
        pattern = self.pattern
        if self.ignorecase:
            name = name.lower()
            pattern = pattern.lower()

        match self.mode:
            case "exact":
                return name == pattern
            case "startswith":
                return name.startswith(pattern)
            case "endswith":
                return name.endswith(pattern)
            case "contains":
                return pattern in name
            case "regex":
                return bool(self._regex.search(name))
            case _:
                return False
