from __future__ import annotations

from contextlib import suppress
from gzip import open as gzip_open
from pathlib import Path
from shutil import copyfileobj

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.record import Record
from turboprint_logger.handlers.file import FileHandler
from turboprint_logger.interfaces import Filter, Formatter

__all__ = ("RotatingFileHandler",)


class RotatingFileHandler(FileHandler):
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
        self.compress = compress
        self.max_bytes = max_bytes
        self.max_lines = max_lines
        self.backup_count = backup_count
        self._line_count = 0
        self._current_size = 0
        self._update_counts()

    def _update_counts(self) -> None:
        with self._lock:
            path = Path(self.file_path)
            if path.exists():
                self._current_size = path.stat().st_size
                if self.max_lines is not None:
                    try:
                        with path.open("r", encoding=self.encoding) as file:
                            self._line_count = len(file.readlines())
                    except OSError:
                        self._line_count = 0
                else:
                    self._line_count = 0
            else:
                self._current_size = 0
                self._line_count = 0

    def _should_rotate(self, record: Record) -> bool:  # noqa: ARG002
        if self.max_bytes is not None and self._current_size >= self.max_bytes:
            return True
        return bool(self.max_lines is not None and self._line_count >= self.max_lines)

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
                with dst.open("rb") as f_in, gzip_open(compressed_path, "wb") as f_out:
                    copyfileobj(f_in, f_out)
                dst.unlink(missing_ok=True)

    def _write(self, record: Record) -> None:
        with self._lock:
            if self._should_rotate(record):
                self.close()
                self._rotate()
                self._open_file()
                self._closed = False
                self._update_counts()

            super()._write(record)

            formatter = self.formatter or record.logger.formatter.get()
            line = formatter.format(record) + self.separator
            self._current_size += len(line.encode(self.encoding))
            if self.max_lines is not None:
                self._line_count += 1

    def reopen(self) -> None:
        super().reopen()
        self._update_counts()
