from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from string import Template
from time import sleep
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, LevelType
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
        success_level: LevelType = Level.SUCCESS,
        success_message: str = "${function} succeeded after ${attempt} attempt",
        warning_level: LevelType = Level.WARNING,
        warning_message: str = "Attempt ${attempt} for ${function} failed[${exception_type}]: ${exception}",  # noqa: E501
        error_level: LevelType = Level.ERROR,
        error_message: str = "Function ${function} failed after ${attempt} attempt",
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.max_attempts = max(1, max_attempts)
        self.delay = max(0.0, delay)
        self.backoff = max(0.0, backoff)
        self.exceptions = exceptions
        self.success_level = success_level
        self.success_message = Template(success_message)
        self.warning_level = warning_level
        self.warning_message = Template(warning_message)
        self.error_level = error_level
        self.error_message = Template(error_message)

    def _log_warning(self, func_name: str, attempt: int, exc: Exception) -> None:
        self.logger(
            self.warning_level,
            self.warning_message.safe_substitute(
                function=func_name,
                attempt=attempt,
                exception_type=exc.__class__.__name__,
                exception=exc,
            ),
        )

    def _log_success(self, func_name: str, attempt: int) -> None:
        if attempt > 1:
            self.logger(
                self.success_level,
                self.success_message.safe_substitute(
                    function=func_name, attempt=attempt
                ),
            )

    def _log_error(self, func_name: str, attempt: int) -> None:
        self.logger(
            self.error_level,
            self.error_message.safe_substitute(function=func_name, attempt=attempt),
        )

    def _raise_final(self, func_name: str, last_exc: Exception | None) -> None:
        if last_exc:
            msg = f"{func_name}, last exception {last_exc.__class__.__name__}: {last_exc}"  # noqa: E501
            raise RetryLimitExceededError(msg) from last_exc
        msg = "Unknown error in retry"
        raise UnknownRetryError(msg)

    def __call__(self, func: _F) -> _F:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
                last_exc: Exception | None = None
                for attempt in range(1, self.max_attempts + 1):
                    try:
                        result = await func(*args, **kwargs)
                        self._log_success(func.__name__, attempt)
                        return result  # noqa: TRY300
                    except self.exceptions as exc:
                        last_exc = exc  # ty:ignore[invalid-assignment]
                        self._log_warning(
                            func.__name__,
                            attempt,
                            exc,  # ty:ignore[invalid-argument-type]
                        )
                        if attempt < self.max_attempts:
                            await asyncio.sleep(
                                self.delay * (self.backoff ** (attempt - 1))
                            )
                self._log_error(func.__name__, attempt)
                self._raise_final(func.__name__, last_exc)
                return None

            return cast(_F, async_wrapper)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            last_exc: Exception | None = None
            for attempt in range(1, self.max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    self._log_success(func.__name__, attempt)
                    return result  # noqa: TRY300
                except self.exceptions as exc:
                    last_exc = exc  # ty:ignore[invalid-assignment]
                    self._log_warning(
                        func.__name__,
                        attempt,
                        exc,  # ty:ignore[invalid-argument-type]
                    )
                    if attempt < self.max_attempts:
                        sleep(self.delay * (self.backoff ** (attempt - 1)))
            self._log_error(func.__name__, attempt)
            self._raise_final(func.__name__, last_exc)
            return None

        return cast(_F, wrapper)


retry = RetryDecorator
