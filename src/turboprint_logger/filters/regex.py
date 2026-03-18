from __future__ import annotations

from re import IGNORECASE, Pattern
from re import compile as re_compile
from typing import Literal

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

_FIELDS = Literal[
    "message", "level_name", "logger_name", "code", "file", "function", "line"
]


class RegexFilter(Filter):
    def __init__(
        self,
        pattern: str | Pattern,
        field: _FIELDS | str = "message",
        *,
        ignorecase: bool = True,
    ) -> None:
        if isinstance(pattern, Pattern):
            self.regex = pattern
        else:
            flags = IGNORECASE if ignorecase else 0
            self.regex = re_compile(pattern, flags)
        self.field = field
        self.ignorecase = ignorecase

    def _get_field_value(self, record: Record) -> str:  # noqa: PLR0911
        match self.field.lower():
            case "message":
                return (
                    record.message() if callable(record.message) else record.message  # ty:ignore[call-top-callable]
                )
            case "level_name":
                return record.level.name
            case "logger_name":
                return record.logger.name
            case "file":
                return record.file or ""
            case "function":
                return record.function or ""
            case "line":
                return str(record.line) if record.line else ""
            case _:
                return str(record.context.get(self.field, ""))

    def filter(self, record: Record) -> bool:
        text = self._get_field_value(record)
        return bool(self.regex.search(text))
