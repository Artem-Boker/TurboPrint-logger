from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from turboprint_logger.core.levels import LevelRegistry

if TYPE_CHECKING:
    from turboprint_logger.core.logger import Logger


@dataclass(slots=True)
class Record:
    message: str | Callable[[], str]
    level: LevelRegistry
    logger: Logger
    trace_id: int
    logger_id: int
    file: str
    function: str
    line: int
    date_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    context: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

    def copy(self) -> Record:
        return Record(
            message=self.message,
            level=self.level,
            logger=self.logger,
            trace_id=self.trace_id,
            logger_id=self.logger_id,
            file=self.file,
            function=self.function,
            line=self.line,
            date_time=self.date_time,
            context=self.context.copy(),
            tags=self.tags.copy(),
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message}, "
            f"level={self.level}, "
            f"logger={self.logger})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message}, "
            f"level={self.level!r}, "
            f"logger={self.logger!r}, "
            f"trace_id={self.trace_id}, "
            f"logger_id={self.logger_id}, "
            f"context_keys={tuple(self.context.keys())}, "
            f"tags={tuple(self.tags)}, "
            f"file={self.file}, "
            f"function={self.function}, "
            f"line={self.line})"
        )
