from __future__ import annotations

from sys import stdout as default_output
from threading import RLock, Timer
from typing import TextIO

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers.stream import (
    InvalidBufferSizeError,
    InvalidStreamError,
    InvalidStreamFlushIntervalError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("BufferedStreamHandler",)


class BufferedStreamHandler(Handler):
    def __init__(  # noqa: PLR0913
        self,
        stream: TextIO = default_output,
        buffer_size: int = 1_000,
        flush_interval: int = 60,
        min_level: LevelType = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        super().__init__(min_level, formatter, filters)
        if not callable(getattr(stream, "write", None)):
            msg = "stream must provide a callable 'write' method"
            raise InvalidStreamError(msg)
        if not callable(getattr(stream, "flush", None)):
            msg = "stream must provide a callable 'flush' method"
            raise InvalidStreamError(msg)
        if not isinstance(buffer_size, int):
            msg = "buffer_size must be an integer"
            raise InvalidBufferSizeError(msg)
        if buffer_size < 1:
            msg = "buffer_size must be greater than 0"
            raise InvalidBufferSizeError(msg)
        if not isinstance(flush_interval, int | float):
            msg = "flush_interval must be a number"
            raise InvalidStreamFlushIntervalError(msg)
        if flush_interval <= 0:
            msg = "flush_interval must be greater than 0"
            raise InvalidStreamFlushIntervalError(msg)
        self.stream = stream
        self.buffer: list[str] = []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self._timer: Timer | None = None
        self._closed = False
        self._lock = RLock()
        self._schedule_flush()

    def _schedule_flush(self) -> None:
        with self._lock:
            if self._closed:
                return
            timer = Timer(interval=self.flush_interval, function=self._on_timer_flush)
            timer.daemon = True
            self._timer = timer
            timer.start()

    def _on_timer_flush(self) -> None:
        try:
            self.flush()
        finally:
            with self._lock:
                if not self._closed:
                    self._schedule_flush()

    def emit(self, record: Record) -> None:
        with self._lock:
            formatter = self.formatter or record.logger.formatter.get()
            self.buffer.append(formatter.format(record))
            if len(self.buffer) >= self.buffer_size:
                self.flush()

    def flush(self) -> None:
        with self._lock:
            if self.buffer:
                data = "\n".join(self.buffer) + "\n"
                self.buffer.clear()
                self.stream.write(data)
                self.stream.flush()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            self.flush()
