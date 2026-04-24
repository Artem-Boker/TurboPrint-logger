from __future__ import annotations

from contextlib import contextmanager
from threading import local
from typing import Literal

from turboprint_logger.managers._mixins import TemporaryMixin

__all__ = ("LocaleManager",)

_SUPPORTED_LANGUAGES = Literal["ru_RU", "en_US"]


class LocaleManager(TemporaryMixin[_SUPPORTED_LANGUAGES]):
    _thread_local = local()

    @classmethod
    def get(cls) -> _SUPPORTED_LANGUAGES:
        return getattr(cls._thread_local, "language", "en_US")

    @classmethod
    def set(cls, language: _SUPPORTED_LANGUAGES) -> None:
        cls._thread_local.language = language

    @classmethod
    @contextmanager
    def temporary(cls, item: _SUPPORTED_LANGUAGES):  # noqa: ANN206
        if not hasattr(cls._thread_local, "stack"):
            cls._thread_local.stack = []
        cls._thread_local.stack.append(cls.get())
        cls.set(item)
        try:
            yield
        finally:
            cls.set(cls._thread_local.stack.pop())

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(locale="{self.get()}")'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(locale="{self.get()}")'
