from __future__ import annotations

from contextlib import contextmanager
from threading import local
from typing import Literal

__all__ = ("LocaleManager",)

_SUPPORTED_LANGUAGES = Literal["ru_RU", "en_US"]


class LocaleManager:
    _local = local()

    @classmethod
    def get(cls) -> _SUPPORTED_LANGUAGES:
        return getattr(cls._local, "language", "en_US")

    @classmethod
    def set(cls, language: _SUPPORTED_LANGUAGES) -> None:
        cls._local.language = language

    @classmethod
    @contextmanager
    def temporary(cls, language: _SUPPORTED_LANGUAGES):  # noqa: ANN206
        if not hasattr(cls._local, "stack"):
            cls._local.stack = []
        snapshot = cls.get()
        cls._local.stack.append(snapshot)
        cls.set(language)
        try:
            yield
        finally:
            cls.set(cls._local.stack.pop())

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(locale="{self.get()}")'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(locale="{self.get()}")'
