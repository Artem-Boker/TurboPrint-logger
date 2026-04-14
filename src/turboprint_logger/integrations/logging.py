from __future__ import annotations

import logging
from typing import Any

from turboprint_logger.utils.reserved import filter_reserved
from turboprint_logger.core.levels import Level, Level
from turboprint_logger.core.logger import Logger

__all__ = ("LoggingAdapter", "install_adapter")

_STD_TO_CUSTOM_LEVEL = {
    logging.NOTSET: Level.NOTSET,
    logging.DEBUG: Level.DEBUG,
    logging.INFO: Level.INFO,
    logging.WARN: Level.WARNING,
    logging.WARNING: Level.WARNING,
    logging.ERROR: Level.ERROR,
    logging.FATAL: Level.CRITICAL,
    logging.CRITICAL: Level.CRITICAL,
}


class LoggingAdapter(logging.Handler):
    def __init__(self, level: int = logging.NOTSET) -> None:
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            custom_logger = Logger.get_logger(record.name)
        except Exception:
            self.handleError(record)
            return
        level = self._convert_level(record.levelno)
        message = record.getMessage()
        extra = filter_reserved(self._extract_extra(record))
        custom_logger(level, message, **extra)

    def _convert_level(self, levelno: int) -> Level:
        if levelno in _STD_TO_CUSTOM_LEVEL:
            return _STD_TO_CUSTOM_LEVEL[levelno]

        custom_level = Level.get_by_level(levelno)
        if custom_level is not None:
            return custom_level

        return Level.NOTSET

    def _extract_extra(self, record: logging.LogRecord) -> dict[str, Any]:
        std_attrs = {
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack_info",
            "taskName",
            "thread",
            "threadName",
        }
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in std_attrs and not key.startswith("_")
        }


def install_adapter(level: int = logging.NOTSET) -> LoggingAdapter:
    handler = LoggingAdapter(level)
    logging.root.addHandler(handler)
    return handler
