from __future__ import annotations

from contextlib import suppress
from gzip import open as gzip_open
from pathlib import Path
from shutil import copyfileobj
from time import time
from typing import Literal

from turboprint_logger.core.levels import Level, Level
from turboprint_logger.core.record import Record
from turboprint_logger.handlers.file import FileHandler
from turboprint_logger.interfaces import Filter, Formatter

__all__ = ("TimedRotatingFileHandler",)


class TimedRotatingFileHandler(FileHandler):
    def __init__(  # noqa: PLR0913
        self,
        file_path: str,
        min_level: Level = Level.NOTSET,
        formatter: Formatter | None = None,
        filters: list[Filter] | None = None,
        *,
        separator: str = "\n",
        buffer_size: int | None = None,
        encoding: str = "utf-8",
        update_mode: bool = False,
        compress: bool = True,
        when: Literal["s", "m", "h", "D", "W", "M"] = "h",
        interval: int = 1,
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
        self.when = when.strip()
        self.interval = max(1, interval)
        self.backup_count = backup_count
        self._rotation_seconds = self._get_rotation_seconds()
        self._rollover_at = self._compute_rollover()

    def _get_rotation_seconds(self) -> int:
        multipliers = {
            "s": 1,
            "m": 60,
            "h": 60 * 60,
            "D": 60 * 60 * 24,
            "W": 60 * 60 * 24 * 7,
            "M": 60 * 60 * 24 * 30,
        }
        return multipliers.get(self.when, multipliers["h"]) * self.interval

    def _compute_rollover(self) -> float:
        return time() + self._rotation_seconds

    def _should_rotate(self) -> bool:
        return time() >= self._rollover_at

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
                except Exception:
                    with suppress(OSError):
                        compressed_path.unlink(missing_ok=True)

    def _write(self, record: Record) -> None:
        with self._lock:
            if self._should_rotate():
                self.close()
                self._rotate()
                self._open_file()
                self._closed = False
                self._schedule_flush()
                self._rollover_at = self._compute_rollover()

            super()._write(record)
