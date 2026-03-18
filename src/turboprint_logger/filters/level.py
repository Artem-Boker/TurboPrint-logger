from __future__ import annotations

from turboprint_logger.core.levels import LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter


class LevelFilter(Filter):
    def __init__(
        self,
        min_level: LevelRegistry | None = None,
        max_level: LevelRegistry | None = None,
        allowed_levels: list[LevelRegistry] | None = None,
    ) -> None:
        self.min_level = min_level
        self.max_level = max_level
        self.allowed_levels = allowed_levels

    def filter(self, record: Record) -> bool:
        level = record.level

        if self.min_level and level.level < self.min_level.level:
            return False

        if self.max_level and level.level > self.max_level.level:
            return False

        return not (self.allowed_levels and level not in self.allowed_levels)
