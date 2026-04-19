from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from string import Template
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.logger import Logger

__all__ = ("deprecated",)

_F = TypeVar("_F", bound=Callable[..., Any])


class DeprecatedDecorator:
    def __init__(
        self,
        message: str = "The ${function} function has been deprecated and will be removed in a future release.",  # noqa: E501
        logger: str | Logger | None = None,
        level: LevelType = Level.WARNING,
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.message = Template(message)
        self.level = level

    def __call__(self, func: _F) -> _F:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
                self.logger(
                    self.level,
                    self.message.safe_substitute(function=func.__name__),
                )
                return await func(*args, **kwargs)

            return cast(_F, async_wrapper)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            self.logger(
                self.level,
                self.message.safe_substitute(function=func.__name__),
            )
            return func(*args, **kwargs)

        return cast(_F, wrapper)


deprecated = DeprecatedDecorator
