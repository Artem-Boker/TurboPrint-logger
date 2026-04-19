from __future__ import annotations

from contextlib import suppress
from gzip import open as gzip_open
from pathlib import Path
from shutil import copyfileobj

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.record import Record
from turboprint_logger.exceptions.handlers.file import (
    FileClosedError,
    FileHandlerConfigError,
    FileWriteError,
)
from turboprint_logger.handlers.file import FileHandler
from turboprint_logger.interfaces import Filter, Formatter

__all__ = ("RotatingFileHandler",)


class RotatingFileHandler(FileHandler):
    def __init__(  # noqa: PLR0913
        self,
        file_path: str,
        min_level: LevelType = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
        *,
        separator: str = "\n",
        buffer_size: int | None = None,
        encoding: str = "utf-8",
        update_mode: bool = False,
        compress: bool = True,
        max_bytes: int | None = None,
        max_lines: int | None = None,
        backup_count: int = 0,
    ) -> None:
        super().__init__(
            file_path=file_path,
            min_level=min_level,
            formatter=formatter,
            filters=filters,
            separator=separator,
            buffer_size=buffer_size,
            encoding=encoding,
            update_mode=update_mode,
        )
        if max_bytes is None and max_lines is None:
            msg = f"{self.__class__.__name__} required at least one of max_bytes or max_lines"  # noqa: E501
            raise FileHandlerConfigError(msg)
        self.compress = compress
        self.max_bytes = max_bytes
        self.max_lines = max_lines
        self.backup_count = backup_count
        self._line_count = 0
        self._current_size = 0
        self._update_counts()

    def _update_counts(self) -> None:
        path = Path(self.file_path)
        size = 0
        line_count = 0
        with self._lock:
            if path.exists():
                size = path.stat().st_size
                if self.max_lines is not None:
                    try:
                        with path.open("r", encoding=self.encoding) as file:
                            line_count = sum(1 for _ in file)
                    except OSError:
                        line_count = 0
            self._current_size = size
            self._line_count = line_count

    def _should_rotate(self, _record: Record) -> bool:
        with self._lock:
            if self.max_bytes is not None and self._current_size >= self.max_bytes:
                return True
            return self.max_lines is not None and self._line_count >= self.max_lines

    def _rotated_path(self, number: int) -> Path:
        path = Path(self.file_path)
        suffixes = path.suffixes
        stem = path.name.removesuffix("".join(suffixes)) if suffixes else path.name
        new_name = f"{stem}.{number}{''.join(suffixes)}"
        return path.parent / new_name

    @staticmethod
    def _compressed_path(path: Path) -> Path:
        return path.with_suffix(path.suffix + ".gz")

    def _rotate(self) -> None:
        with self._lock:
            if self.backup_count <= 0:
                with suppress(OSError):
                    Path(self.file_path).unlink(missing_ok=True)
                return

            for i in range(self.backup_count - 1, 0, -1):
                src = self._rotated_path(i)
                dst = self._rotated_path(i + 1)
                src_gz = self._compressed_path(src)
                dst_gz = self._compressed_path(dst)
                if src_gz.exists():
                    with suppress(OSError):
                        src_gz.replace(dst_gz)
                elif src.exists():
                    with suppress(OSError):
                        src.replace(dst)

            src = Path(self.file_path)
            dst = self._rotated_path(1)
            if src.exists():
                with suppress(OSError):
                    src.replace(dst)

            if self.compress and dst.exists():
                compressed_path = self._compressed_path(dst)
                try:
                    with (
                        dst.open("rb") as f_in,
                        gzip_open(compressed_path, "wb") as f_out,
                    ):
                        copyfileobj(f_in, f_out)
                    dst.unlink(missing_ok=True)
                except Exception:  # noqa: BLE001
                    with suppress(OSError):
                        compressed_path.unlink(missing_ok=True)

    def _write(self, record: Record) -> None:
        with self._lock:
            if self._should_rotate(record):
                self.close()
                self._rotate()
                self._open_file()
                self._closed = False
                self._schedule_flush()
                self._update_counts()

            formatter = self.formatter or record.logger.formatter.get()
            line = formatter.format(record) + self.separator
            if self._file and not self._file.closed:
                try:
                    self._file.write(line)
                except Exception as exc:
                    msg = f"Could not write to file {self.file_path}: {exc}"
                    raise FileWriteError(msg) from exc
            else:
                msg = f"File {self.file_path} is closed"
                raise FileClosedError(msg)
            self._current_size += len(line.encode(self.encoding))
            if self.max_lines is not None:
                self._line_count += 1

    def reopen(self) -> None:
        super().reopen()
        self._update_counts()
