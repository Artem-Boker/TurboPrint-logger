from __future__ import annotations

from re import Pattern
from re import compile as re_compile

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Formatter


class RegexFormatter(Formatter):
    def __init__(
        self,
        pattern: str | Pattern[str],
        replacement: str = "",
        flags: int = 0,
    ) -> None:
        if isinstance(pattern, str):
            self.pattern = re_compile(pattern, flags)
        else:
            self.pattern = pattern
        self.replacement = replacement

    def format(self, record: Record) -> str:
        message = record.message() if callable(record.message) else record.message  # ty:ignore[call-top-callable]
        return self.pattern.sub(self.replacement, message)
