from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from os import getpid
from socket import gethostname
from sys import exc_info
from threading import get_ident
from types import TracebackType
from typing import TYPE_CHECKING, Any, TypeAlias

from turboprint_logger.core.levels import LevelRegistry

if TYPE_CHECKING:
    from turboprint_logger.core.logger import Logger

__all__ = ("Record",)

_HOSTNAME = gethostname()
ExcInfo: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]
)


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
    process_name: str = field(default_factory=lambda: _HOSTNAME)
    process_id: int = field(default_factory=getpid)
    thread_id: int = field(default_factory=get_ident)
    exception_info: ExcInfo = field(default_factory=exc_info)

    def copy(self) -> Record:
        return replace(
            self,
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
            f"line={self.line}, "
            f"process_name={self.process_name!r}, "
            f"process_id={self.process_id}, "
            f"thread_id={self.thread_id}, "
            f"exception_info={self.exception_info})"
        )
