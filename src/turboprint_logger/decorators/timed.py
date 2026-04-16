from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from string import Template
from time import perf_counter
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level
from turboprint_logger.core.logger import Logger

__all__ = ("timed",)

_F = TypeVar("_F", bound=Callable[..., Any])


class TimedDecorator:
    def __init__(
        self,
        logger: str | Logger | None = None,
        level: Level = Level.EVENT,
        message: str = "${function} completed in ${duration}",
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
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN202
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
                )

        return cast(_F, wrapper)


timed = TimedDecorator
