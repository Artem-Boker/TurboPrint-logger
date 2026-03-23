from __future__ import annotations

from datetime import datetime
from string import Template
from typing import TYPE_CHECKING, Any, TypedDict

from colorama import Style

from turboprint_logger.core.levels import LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Formatter

if TYPE_CHECKING:
    from turboprint_logger.core.logger import Logger

__all__ = ("SimpleFormatter",)


class FormatDict(TypedDict):
    message: str
    level: LevelRegistry
    level_name: str
    level_value: int
    level_emoji: str | None
    logger: Logger
    logger_name: str
    date: str
    time: str
    datetime: datetime
    trace_id: int
    logger_id: int
    context: dict[str, Any]
    tags: set[str]
    file: str
    function: str
    line: int


class SimpleFormatter(Formatter):
    def __init__(
        self,
        template: str = "[${date} ${time}] ${logger_name} | ${level_name}: ${message}",
        date_format: str | None = None,
        time_format: str | None = None,
        *,
        colored: bool = False,
    ) -> None:
        self.template = Template(template)
        self.date_format = date_format
        self.time_format = time_format
        self.colored = colored

    def format(self, record: Record) -> str:
        message = record.message() if callable(record.message) else record.message  # ty:ignore[call-top-callable]
        message = Template(message).safe_substitute(record.context)

        date = record.date_time.date()
        date_str = (
            date.strftime(self.date_format) if self.date_format else date.isoformat()
        )

        time = record.date_time.time()
        time_str = (
            time.strftime(self.time_format) if self.time_format else time.isoformat()
        )

        record_format = FormatDict(
            message=message,
            level=record.level,
            level_name=record.level.name,
            level_value=record.level.level,
            level_emoji=record.level.emoji,
            logger=record.logger,
            logger_name=record.logger.name,
            date=date_str,
            time=time_str,
            datetime=record.date_time,
            trace_id=record.trace_id,
            logger_id=record.logger_id,
            context=record.context,
            tags=record.tags,
            file=record.file,
            function=record.function,
            line=record.line,
        )

        output = self.template.safe_substitute(record_format)

        return (
            f"{record.level.color}{output}{Style.RESET_ALL}" if self.colored else output
        )
