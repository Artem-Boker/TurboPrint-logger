from __future__ import annotations

from functools import wraps
from inspect import iscoroutinefunction
from string import Template
from typing import Any, cast

from turboprint_logger.core.levels import Level, LevelType
from turboprint_logger.core.logger import Logger
from turboprint_logger.decorators._callables import FuncT

__all__ = ("deprecated",)

_STACKLEVEL = 3


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

    def __call__(self, func: FuncT) -> FuncT:
        if iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
                self.logger(
                    self.level,
                    self.message.safe_substitute(function=func.__name__),
                    stacklevel=_STACKLEVEL,
                )
                return await func(*args, **kwargs)

            return cast(FuncT, async_wrapper)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            self.logger(
                self.level,
                self.message.safe_substitute(function=func.__name__),
                stacklevel=_STACKLEVEL,
            )
            return func(*args, **kwargs)

        return cast(FuncT, wrapper)


deprecated = DeprecatedDecorator
