from __future__ import annotations

from pathlib import Path
from sys import stderr
from threading import RLock, Timer
from typing import IO

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers import (
    CloseException,
    FileClosedError,
    FileOpenError,
    FileWriteError,
    InvalidFlushIntervalError,
    InvalidSeparatorError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("FileHandler",)


class FileHandler(Handler):
    def __init__(  # noqa: PLR0913
        self,
        file_path: str | Path,
        level: LevelType = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
        *,
        separator: str = "\n",
        buffer_size: int | None = None,
        flush_interval: int = 60,
        encoding: str = "utf-8",
        update_mode: bool = False,
    ) -> None:
        super().__init__(level, formatter, filters)
        if not isinstance(separator, str):
            msg = "separator must be a string"
            raise InvalidSeparatorError(msg)
        if not isinstance(flush_interval, int | float):
            msg = "flush_interval must be a number"
            raise InvalidFlushIntervalError(msg)
        if flush_interval <= 0:
            msg = "flush_interval must be greater than 0"
            raise InvalidFlushIntervalError(msg)
        if not separator:
            msg = "separator must be a non-empty string"
            raise InvalidSeparatorError(msg)

        if buffer_size is None:
            self.buffer_size = -1
        elif buffer_size < 1:
            self.buffer_size = 1
        else:
            self.buffer_size = buffer_size

        self.file_path = Path(file_path)
        self.mode = "a" if update_mode else "w"
        self.encoding = encoding
        self.separator = separator
        self.flush_interval = flush_interval
        self._timer: Timer | None = None
        self._closed = False
        self._file: IO | None = None
        self._lock = RLock()
        self._open_file()
        self._schedule_flush()

    def _schedule_flush(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._timer is not None:
                self._timer.cancel()
            timer = Timer(interval=self.flush_interval, function=self._flush)
            timer.daemon = True
            self._timer = timer
            timer.start()

    def _flush(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._file and not self._file.closed:
                self._file.flush()
            self._schedule_flush()

    def _open_file(self) -> None:
        with self._lock:
            try:
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                self.file_path.touch(exist_ok=True)
                self._file = self.file_path.open(
                    self.mode, encoding=self.encoding, buffering=self.buffer_size
                )
            except Exception as exc:
                msg = f"Could not open file {self.file_path}: {exc}"
                raise FileOpenError(msg) from exc

    def reopen(self) -> None:
        with self._lock:
            if self._file and not self._file.closed:
                self._file.close()
            self._file = None
            self._closed = False
            original_mode = self.mode
            self.mode = "a"
            try:
                self._open_file()
            finally:
                self.mode = original_mode
            self._schedule_flush()

    def close(self) -> None:
        try:
            with self._lock:
                self._closed = True
                if self._timer is not None:
                    self._timer.cancel()
                    self._timer = None
                if self._file and not self._file.closed:
                    self._file.close()
                self._file = None
        except Exception as exc:
            msg = f"Could not close file {self.file_path}: {exc}"
            raise CloseException(msg) from exc

    def _write(self, record: Record) -> None:
        with self._lock:
            if self._file is None or self._file.closed:
                self._open_file()
            formatter = self.formatter or record.logger.formatter.get()
            if self._file and not self._file.closed:
                try:
                    self._file.write(formatter.format(record) + self.separator)
                except Exception as exc:
                    msg = f"Could not write to file {self.file_path}: {exc}"
                    raise FileWriteError(msg) from exc
            else:
                msg = f"File {self.file_path} is closed"
                raise FileClosedError(msg)

    def emit(self, record: Record) -> None:
        try:
            self._write(record)
        except Exception as exc:  # noqa: BLE001
            stderr.write(
                f"{exc.__class__.__name__}[{self.__class__.__name__}]: {exc}\n"
            )
            try:
                self.reopen()
                self._write(record)
            except Exception as exc:  # noqa: BLE001
                stderr.write(
                    f"{exc.__class__.__name__}[{self.__class__.__name__}]: Re-open to {self.file_path} failed: {exc}\n"  # noqa: E501
                )
