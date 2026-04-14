from __future__ import annotations

from turboprint_logger.core.levels import Level
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("LevelFilter",)


class LevelFilter(Filter):
    def __init__(
        self,
        min_level: Level | None = None,
        max_level: Level | None = None,
        allowed_levels: list[Level] | None = None,
    ) -> None:
        self.min_level = min_level
        self.max_level = max_level
        self.allowed_levels = allowed_levels

    def filter(self, record: Record) -> bool:
        level = record.level

        if self.min_level is not None and level.level < self.min_level.level:
            return False
        if self.max_level is not None and level.level > self.max_level.level:
            return False

        return not (self.allowed_levels and level not in self.allowed_levels)
