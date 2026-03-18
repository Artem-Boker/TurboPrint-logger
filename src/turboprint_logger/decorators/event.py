from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from itertools import chain
from string import Template
from time import perf_counter
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.logger import Logger

_F = TypeVar("_F", bound=Callable[..., Any])

_RESERVED_PARAMS = {"level", "message", "tags"}


class EventDecorator:
    def __init__(  # noqa: PLR0913
        self,
        logger: str | Logger | None = None,
        level: LevelRegistry = Level.EVENT,
        error_level: LevelRegistry = Level.ERROR,
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
        self.entry_message = Template(entry_message)
        self.exit_message = Template(exit_message)
        self.exc_message = Template(exc_message)
        self.default_context = default_context

    @staticmethod
    def _filter_reserved(extra: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in extra.items() if k not in _RESERVED_PARAMS}

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
            entry_message = self.entry_message.safe_substitute(entry_extra)
            self.logger(
                self.level,
                entry_message,
                **self._filter_reserved(entry_extra),
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
                exc_message = self.exc_message.safe_substitute(exc_extra)
                self.logger(
                    self.error_level,
                    exc_message,
                    **self._filter_reserved(exc_extra),
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
            exit_message = self.exit_message.safe_substitute(exit_extra)
            self.logger(
                self.level,
                exit_message,
                **self._filter_reserved(exit_extra),
            )
            return result

        return cast(_F, wrapper)


event = EventDecorator
