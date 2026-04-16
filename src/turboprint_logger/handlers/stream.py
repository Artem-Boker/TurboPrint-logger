from __future__ import annotations

from contextlib import suppress
from sys import stdout as default_output
from threading import RLock
from typing import TextIO

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers.stream import InvalidStreamError
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("StreamHandler",)


class StreamHandler(Handler):
    def __init__(
        self,
        stream: TextIO = default_output,
        min_level: LevelRegistry = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        super().__init__(min_level, formatter, filters)
        if not callable(getattr(stream, "write", None)):
            msg = "stream must provide a callable 'write' method"
            raise InvalidStreamError(msg)
        self.stream = stream
        self._lock = RLock()

    def emit(self, record: Record) -> None:
        with self._lock:
            formatter = self.formatter or record.logger.formatter.get()
            with suppress(OSError):
                self.stream.write(formatter.format(record) + "\n")

    def close(self) -> None:
        with self._lock:
            self.stream.flush()
