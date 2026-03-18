from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import ClassVar

from colorama import Fore, Style
from emoji import LANGUAGES as EMOJI_LANGUAGES
from emoji import emojize, is_emoji

from turboprint_logger.exceptions.core.levels import (
    InvalidLevelColorError,
    InvalidLevelEmojiError,
    LevelNameAlreadyExistsError,
    LevelValueAlreadyExistsError,
    NegativeLevelError,
)
from turboprint_logger.utils.normalizers import normalize_level_name


@dataclass(frozen=True, slots=True)
class LevelRegistry:
    name: str
    level: int
    color: str
    emoji: str | None = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}[{self.level}])"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f'name="{self.name}", '
            f"level={self.level}, "
            f"emoji={self.emoji})"
        )

    def enabled_for(self, level: LevelRegistry) -> bool:
        return self.level >= level.level


def _register_levels(cls: type[Level]) -> type[Level]:
    for attr_name in dir(cls):
        level = getattr(cls, attr_name)
        if isinstance(level, LevelRegistry):
            cls._by_name[level.name] = level
            cls._by_level[level.level] = level
    return cls


@_register_levels
class Level:
    NOTSET = LevelRegistry("NOTSET", 0, Fore.RESET)
    VERBOSE = LevelRegistry("VERBOSE", 10, Fore.LIGHTBLACK_EX)
    DEBUG = LevelRegistry("DEBUG", 20, Fore.MAGENTA)
    TRACE = LevelRegistry("TRACE", 30, Fore.BLUE)
    LOG = LevelRegistry("LOG", 40, Fore.CYAN)
    NOTICE = LevelRegistry("NOTICE", 50, Fore.LIGHTYELLOW_EX)
    EVENT = LevelRegistry("EVENT", 60, Fore.LIGHTCYAN_EX)
    PERFORMANCE = LevelRegistry("PERFORMANCE", 70, Fore.CYAN)
    SUCCESS = LevelRegistry("SUCCESS", 80, Fore.GREEN)
    SECURITY = LevelRegistry("SECURITY", 90, Fore.LIGHTGREEN_EX)
    AUDIT = LevelRegistry("AUDIT", 100, Fore.YELLOW)
    INFO = LevelRegistry("INFO", 110, Fore.LIGHTBLUE_EX)
    WARNING = LevelRegistry("WARNING", 120, Fore.RED)
    ERROR = LevelRegistry("ERROR", 130, Fore.LIGHTRED_EX)
    ALERT = LevelRegistry("ALERT", 140, Style.BRIGHT + Fore.YELLOW)
    CRITICAL = LevelRegistry("CRITICAL", 150, Style.BRIGHT + Fore.LIGHTRED_EX)
    FATAL = LevelRegistry("FATAL", 160, Style.BRIGHT + Fore.MAGENTA)
    EMERGENCY = LevelRegistry("EMERGENCY", 170, Style.BRIGHT + Fore.RED)

    _by_name: ClassVar[dict[str, LevelRegistry]] = {}
    _by_level: ClassVar[dict[int, LevelRegistry]] = {}

    @classmethod
    @cache
    def get_by_name(cls, name: str) -> LevelRegistry | None:
        return cls._by_name.get(name.strip().upper())

    @classmethod
    @cache
    def get_by_level(cls, level: int) -> LevelRegistry | None:
        return cls._by_level.get(level)

    @classmethod
    @cache
    def all_levels(cls) -> list[LevelRegistry]:
        return sorted(cls._by_level.values(), key=lambda lvl: lvl.level)

    @classmethod
    def register(
        cls,
        name: str,
        level: int,
        color: str = Fore.RESET,
        emoji_name: str | None = None,
    ) -> LevelRegistry:
        name_upper = normalize_level_name(name)
        if name_upper in Level._by_name:
            msg = f'Level with name "{name_upper}" already exists'
            raise LevelNameAlreadyExistsError(msg)
        if level in Level._by_level:
            msg = f"Level with value {level} already exists"
            raise LevelValueAlreadyExistsError(msg)
        if level < 0:
            msg = f'Level "{name_upper}" cannot be negative: {level}'
            raise NegativeLevelError(msg)
        if not isinstance(color, str) or not color:
            msg = f"Invalid color: {color!r}"
            raise InvalidLevelColorError(msg)
        emoji = emoji_name
        if emoji:
            emoji = emoji.strip().lower()
            for lang in EMOJI_LANGUAGES:
                emoji = emojize(
                    emoji, delimiters=("", ""), variant="emoji_type", language=lang
                )
                if is_emoji(emoji):
                    break
            if not is_emoji(emoji):
                msg = f"Invalid emoji code: {emoji_name}"
                raise InvalidLevelEmojiError(msg)

        new_level = LevelRegistry(name_upper, level, color, emoji)
        cls._by_name[name_upper] = new_level
        cls._by_level[level] = new_level
        cls.get_by_name.cache_clear()
        cls.get_by_level.cache_clear()
        cls.all_levels.cache_clear()
        return new_level

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(levels_count={len(self._by_level)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(levels_count={len(self._by_level)})"
