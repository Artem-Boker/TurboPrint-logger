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
    _date_time: datetime | None = field(default=None, init=False, repr=False)
    context: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

    @property
    def date_time(self) -> datetime:
        if self._date_time is None:
            self._date_time = datetime.now(UTC)
        return self._date_time

    @date_time.setter
    def date_time(self, value: datetime) -> None:
        self._date_time = value

    def copy(self) -> Record:
        new = Record(
            message=self.message,
            level=self.level,
            logger=self.logger,
            trace_id=self.trace_id,
            logger_id=self.logger_id,
            context=self.context.copy(),
            tags=self.tags.copy(),
            file=self.file,
            function=self.function,
            line=self.line,
        )
        new._date_time = self._date_time
        return new

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
