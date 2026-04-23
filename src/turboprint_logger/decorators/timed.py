from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from string import Template
from time import perf_counter
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.logger import Logger

__all__ = ("timed",)

_F = TypeVar("_F", bound=Callable[..., Any])
_STACKLEVEL = 3


class TimedDecorator:
    def __init__(
        self,
        logger: str | Logger | None = None,
        level: LevelType = Level.EVENT,
        message: str = "${function} executed in ${duration}s",
        duration_round: int = 3,
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.level = level
        self.message = Template(message)
        self.duration_round = duration_round

    def __call__(self, func: _F) -> _F:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
                start = perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = perf_counter() - start
                    self.logger(
                        self.level,
                        self.message.safe_substitute(
                            function=func.__name__,
                            duration=round(duration, self.duration_round),
                        ),
                        stacklevel=_STACKLEVEL,
                    )

            return cast(_F, async_wrapper)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            start = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = perf_counter() - start
                self.logger(
                    self.level,
                    self.message.safe_substitute(
                        function=func.__name__,
                        duration=round(duration, self.duration_round),
                    ),
                    stacklevel=_STACKLEVEL,
                )

        return cast(_F, wrapper)


timed = TimedDecorator
