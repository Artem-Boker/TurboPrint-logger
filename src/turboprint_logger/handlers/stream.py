from __future__ import annotations

from sys import stderr
from sys import stdout as default_output
from threading import RLock
from typing import TextIO

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers import CloseException, InvalidStreamError
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("StreamHandler",)


class StreamHandler(Handler):
    def __init__(
        self,
        stream: TextIO = default_output,
        level: LevelType = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        super().__init__(level, formatter, filters)
        if not callable(getattr(stream, "write", None)):
            msg = "stream must provide a callable 'write' method"
            raise InvalidStreamError(msg)
        self.stream = stream
        self._lock = RLock()

    def emit(self, record: Record) -> None:
        with self._lock:
            formatter = self.formatter or record.logger.formatter.get()
            try:
                self.stream.write(formatter.format(record) + "\n")
            except Exception as exc:  # noqa: BLE001
                stderr.write(
                    f"{exc.__class__.__name__}[{self.__class__.__name__}]: Failed to write to stream: {exc}\n"  # noqa: E501
                )

    def close(self) -> None:
        try:
            with self._lock:
                self.stream.flush()
        except Exception as exc:
            msg = f"failed to close stream: {exc}"
            raise CloseException(msg) from exc
