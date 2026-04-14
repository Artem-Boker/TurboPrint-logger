from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from itertools import chain
from time import perf_counter
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, Level
from turboprint_logger.core.logger import Logger
from turboprint_logger.utils.reserved import filter_reserved

__all__ = ("event",)

_F = TypeVar("_F", bound=Callable[..., Any])


class EventDecorator:
    def __init__(  # noqa: PLR0913
        self,
        logger: str | Logger | None = None,
        level: Level = Level.EVENT,
        error_level: Level = Level.ERROR,
        arg_parser: Callable[[Any], str] = repr,
        *,
        entry_message: str = "Calling ${function}(${args})",
        exit_message: str = "${function} returned ${result} in ${duration}s",
        exc_message: str = "${function} raised ${exception} in ${duration}s",
        **default_context,
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.level = level
        self.error_level = error_level
        self.arg_parser = arg_parser
        self.entry_message = entry_message
        self.exit_message = exit_message
        self.exc_message = exc_message
        self.default_context = default_context

    def __call__(self, func: _F) -> _F:
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN202
            arg_parts = chain(
                (self.arg_parser(arg) for arg in args),
                (f"{key}={self.arg_parser(value)}" for key, value in kwargs.items()),
            )
            str_args = ", ".join(arg_parts)

            entry_extra: dict[str, Any] = {
                **self.default_context,
                "event": "entry",
                "function": func.__name__,
                "args": str_args,
            }
            self.logger(
                self.level,
                self.entry_message,
                **filter_reserved(entry_extra),
            )
            start_time = perf_counter()

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                end_time = perf_counter()
                exc_extra: dict[str, Any] = {
                    **self.default_context,
                    "event": "exception",
                    "function": func.__name__,
                    "duration": str(round(end_time - start_time, 3)),
                    "exception": repr(exc),
                }
                self.logger(
                    self.error_level,
                    self.exc_message,
                    **filter_reserved(exc_extra),
                )
                raise

            end_time = perf_counter()
            exit_extra: dict[str, Any] = {
                **self.default_context,
                "event": "exit",
                "function": func.__name__,
                "duration": str(round(end_time - start_time, 3)),
                "result": repr(result),
            }
            self.logger(
                self.level,
                self.exit_message,
                **filter_reserved(exit_extra),
            )
            return result

        return cast(_F, wrapper)


event = EventDecorator
