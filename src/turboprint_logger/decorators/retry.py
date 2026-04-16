from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from string import Template
from time import sleep
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level
from turboprint_logger.core.logger import Logger
from turboprint_logger.exceptions.decorators.retry import (
    RetryLimitExceededError,
    UnknownRetryError,
)

__all__ = ("retry",)

_F = TypeVar("_F", bound=Callable[..., Any])


class RetryDecorator:
    def __init__(  # noqa: PLR0913
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
        logger: str | Logger | None = None,
        success_level: Level = Level.SUCCESS,
        success_message: str = "${function} succeeded after ${attempt} attempt",
        warning_level: Level = Level.WARNING,
        warning_message: str = "Attempt ${attempt} for ${function} failed: ${exception}",  # noqa: E501
        error_level: Level = Level.ERROR,
        error_message: str = "Function ${function} failed after ${attempt} attempt",
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.max_attempts = max(1, max_attempts)
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
        self.success_level = success_level
        self.success_message = Template(success_message)
        self.warning_level = warning_level
        self.warning_message = Template(warning_message)
        self.error_level = error_level
        self.error_message = Template(error_message)

    def __call__(self, func: _F) -> _F:
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN202
            last_exc = None
            for attempt in range(1, self.max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        self.logger(
                            self.success_level,
                            self.success_message.safe_substitute(
                                function=func.__name__, attempt=attempt
                            ),
                        )
                except self.exceptions as exc:
                    last_exc = exc
                    self.logger(
                        self.warning_level,
                        self.warning_message.safe_substitute(
                            function=func.__name__, attempt=attempt, exception=exc
                        ),
                    )
                    if attempt < self.max_attempts:
                        sleep(self.delay * (self.backoff ** (attempt - 1)))
                else:
                    return result
            self.logger(
                self.error_level,
                self.error_message.safe_substitute(
                    function=func.__name__, attempt=attempt
                ),
            )
            if last_exc:
                msg = f"{func.__name__}, last exception: {last_exc}"
                raise RetryLimitExceededError(msg) from last_exc
            msg = "Unknown error in retry"
            raise UnknownRetryError(msg)

        return cast(_F, wrapper)


retry = RetryDecorator
