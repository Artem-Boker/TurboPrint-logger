from __future__ import annotations

from atexit import register as register_exit
from pathlib import Path
from sys import stderr
from threading import RLock, Timer
from typing import IO

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers.file import (
    FileClosedError,
    FileOpenError,
    FileWriteError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("FileHandler",)


class FileHandler(Handler):
    def __init__(  # noqa: PLR0913
        self,
        file_path: str,
        min_level: LevelRegistry = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
        *,
        separator: str = "\n",
        buffer_size: int | None = None,
        flush_interval: int = 60,
        encoding: str = "utf-8",
        update_mode: bool = False,
    ) -> None:
        super().__init__(min_level, formatter, filters)
        self.file_path = Path(file_path)
        self.mode = "a" if update_mode else "w"
        self.encoding = encoding
        self.buffer_size = 1 if not buffer_size or buffer_size < 1 else buffer_size
        self.separator = separator
        self.flush_interval = flush_interval
        self._timer: Timer | None = None
        self._closed = False
        self._file: IO | None = None
        self._lock = RLock()
        self._open_file()
        register_exit(self.close)
        self._schedule_flush()

    def _schedule_flush(self) -> None:
        with self._lock:
            if self._closed:
                return
            timer = Timer(interval=self.flush_interval, function=self._flush)
            timer.daemon = True
            self._timer = timer
            timer.start()

    def _flush(self) -> None:
        try:
            with self._lock:
                if self._closed:
                    return
                if self._file and not self._file.closed:
                    self._file.flush()
        finally:
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
            self._open_file()
            if self._timer is None:
                self._schedule_flush()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            if self._file and not self._file.closed:
                self._file.close()
            self._file = None

    def _write(self, record: Record) -> None:
        with self._lock:
            if not self._file:
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
            self.reopen()
            try:
                self._write(record)
            except Exception as exc:  # noqa: BLE001
                stderr.write(
                    f"{exc.__class__.__name__}[{self.__class__.__name__}]: Failed to write to {self.file_path}: {exc}\n"  # noqa: E501
                )
