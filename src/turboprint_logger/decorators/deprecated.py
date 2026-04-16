from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from string import Template
from typing import Any, TypeVar, cast

from turboprint_logger.core.levels import Level
from turboprint_logger.core.logger import Logger

__all__ = ("deprecated",)

_F = TypeVar("_F", bound=Callable[..., Any])


class DeprecatedDecorator:
    def __init__(
        self,
        message: str = "The ${function} function has been deprecated and will be removed in a future release.",  # noqa: E501
        logger: str | Logger | None = None,
        level: Level = Level.EVENT,
    ) -> None:
        self.logger = (
            logger
            if isinstance(logger, Logger)
            else Logger.get_logger(logger or "root")
        )
        self.message = Template(message)
        self.level = level

    def __call__(self, func: _F) -> _F:
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN202
            self.logger(
                self.level, self.message.safe_substitute(function=func.__name__)
            )
            return func(*args, **kwargs)

        return cast(_F, wrapper)


deprecated = DeprecatedDecorator
