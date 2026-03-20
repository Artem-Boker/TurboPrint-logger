from __future__ import annotations

from atexit import register as register_exit
from pathlib import Path
from sys import stderr
from threading import RLock
from typing import IO

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers.file import (
    FileClosedError,
    FileOpenError,
    FileWriteError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler


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
        encoding: str = "utf-8",
        update_mode: bool = False,
    ) -> None:
        super().__init__(min_level, formatter, filters)
        self.file_path = Path(file_path)
        self.mode = "a" if update_mode else "w"
        self.encoding = encoding
        self.buffer_size = 1 if not buffer_size or buffer_size < 1 else buffer_size
        self.separator = separator
        self._file: IO | None = None
        self._lock = RLock()
        self._open_file()
        register_exit(self.close)

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
            self.close()
            self._open_file()

    def close(self) -> None:
        with self._lock:
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
        except OSError:
            self.reopen()
            try:
                self._write(record)
            except OSError:
                stderr.write(
                    f"OSError[FileHandler]: Failed to write to {self.file_path}\n"
                )
