from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from itertools import chain
from time import perf_counter
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.logger import Logger
from turboprint_logger.utils.reserved import filter_reserved

__all__ = ("event",)

_F = TypeVar("_F", bound=Callable[..., Any])


class EventDecorator:
    def __init__(  # noqa: PLR0913
        self,
        logger: str | Logger | None = None,
        level: LevelType = Level.EVENT,
        error_level: LevelType = Level.ERROR,
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

    def _build_entry_extra(
        self,
        func: _F,  # pyright: ignore[reportInvalidTypeVarUse]
        args: tuple[Any],
        kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        arg_parts = chain(
            (self.arg_parser(arg) for arg in args),
            (f"{key}={self.arg_parser(value)}" for key, value in kwargs.items()),
        )
        return filter_reserved(
            {
                **self.default_context,
                "event": "entry",
                "function": func.__name__,
                "args": ", ".join(arg_parts),
            }
        )

    def _build_exit_extra(
        self,
        func: _F,  # pyright: ignore[reportInvalidTypeVarUse]
        duration: float,
        result: Any,  # noqa: ANN401
    ) -> dict[str, Any]:
        return filter_reserved(
            {
                **self.default_context,
                "event": "exit",
                "function": func.__name__,
                "duration": str(round(duration, 3)),
                "result": repr(result),
            }
        )

    def _build_exc_extra(
        self,
        func: _F,  # pyright: ignore[reportInvalidTypeVarUse]
        duration: float,
        exc: BaseException,
    ) -> dict[str, Any]:
        return filter_reserved(
            {
                **self.default_context,
                "event": "exception",
                "function": func.__name__,
                "duration": str(round(duration, 3)),
                "exception": repr(exc),
            }
        )

    def __call__(self, func: _F) -> _F:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
                self.logger(
                    self.level,
                    self.entry_message,
                    **self._build_entry_extra(func, args, kwargs),
                )
                start_time = perf_counter()
                try:
                    result = await func(*args, **kwargs)
                except Exception as exc:
                    duration = perf_counter() - start_time
                    self.logger(
                        self.error_level,
                        self.exc_message,
                        **self._build_exc_extra(func, duration, exc),
                    )
                    raise
                duration = perf_counter() - start_time
                self.logger(
                    self.level,
                    self.exit_message,
                    **self._build_exit_extra(func, duration, result),
                )
                return result

            return cast(_F, async_wrapper)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            self.logger(
                self.level,
                self.entry_message,
                **self._build_entry_extra(func, args, kwargs),
            )
            start_time = perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                duration = perf_counter() - start_time
                self.logger(
                    self.error_level,
                    self.exc_message,
                    **self._build_exc_extra(func, duration, exc),
                )
                raise
            duration = perf_counter() - start_time
            self.logger(
                self.level,
                self.exit_message,
                **self._build_exit_extra(func, duration, result),
            )
            return result

        return cast(_F, wrapper)


event = EventDecorator
