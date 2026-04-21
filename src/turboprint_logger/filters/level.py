from __future__ import annotations

from turboprint_logger.core.levels import LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("LevelFilter",)


class LevelFilter(Filter):
    def __init__(
        self,
        level: LevelType | None = None,
        max_level: LevelType | None = None,
        allowed_levels: list[LevelType] | None = None,
    ) -> None:
        self.level = level
        self.max_level = max_level
        self.allowed_levels = set(allowed_levels) if allowed_levels else None

    def filter(self, record: Record) -> bool:
        level = record.level

        if self.level is not None and level.value < self.level.value:
            return False
        if self.max_level is not None and level.value > self.max_level.value:
            return False

        return not (self.allowed_levels and level not in self.allowed_levels)
