from __future__ import annotations

from atexit import register as register_exit
from sys import stdout as default_output
from threading import RLock, Timer
from typing import TextIO

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter, Formatter, Handler


class BufferedStreamHandler(Handler):
    def __init__(  # noqa: PLR0913
        self,
        stream: TextIO = default_output,
        buffer_size: int = 1_000,
        flush_interval: int = 60,
        min_level: LevelRegistry = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        super().__init__(min_level, formatter, filters)
        self.stream = stream
        self.buffer: list[str] = []
        self.buffer_size = max(buffer_size, 0)
        self._timer = Timer(interval=flush_interval, function=self.flush)
        self._lock = RLock()
        register_exit(lambda: (self._timer.cancel(), self.flush()))
        self._timer.start()

    def emit(self, record: Record) -> None:
        with self._lock:
            formatter = self.formatter or record.logger.formatter.get()
            self.buffer.append(formatter.format(record))
            if len(self.buffer) >= self.buffer_size:
                self.flush()

    def flush(self) -> None:
        with self._lock:
            if self.buffer:
                self.stream.write("\n".join(self.buffer) + "\n")
                self.stream.flush()
                self.buffer.clear()
