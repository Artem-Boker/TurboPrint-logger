from __future__ import annotations

from threading import Lock
from typing import Any

from colorama import Fore, Style
from emoji import emojize, purely_emoji

from turboprint_logger.exceptions.core import (
    InvalidLevelColorError,
    InvalidLevelEmojiError,
    LevelNameAlreadyExistsError,
    LevelValueAlreadyExistsError,
    NegativeLevelError,
)
from turboprint_logger.exceptions.utils import InvalidLevelNameError
from turboprint_logger.utils.normalizers import normalize_level_name

__all__ = ("Level", "LevelType")


class LevelType:
    __slots__ = ("_color", "_emoji", "_name", "_raw_emoji", "_value")

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> int:
        return self._value

    @property
    def color(self) -> str:
        return self._color

    @property
    def emoji(self) -> str | None:
        return self._emoji

    def __init__(
        self, name: str, value: int, color: str, alias_emoji_code: str | None = None
    ) -> None:
        self._name = normalize_level_name(name)
        self._value = value
        self._color = color
        if alias_emoji_code and alias_emoji_code.strip():
            self._raw_emoji = alias_emoji_code.strip().lower()
            self._raw_emoji = (
                ":" + self._raw_emoji
                if not self._raw_emoji.startswith(":")
                else self._raw_emoji
            )
            self._raw_emoji = (
                self._raw_emoji + ":"
                if not self._raw_emoji.endswith(":")
                else self._raw_emoji
            )
        else:
            self._raw_emoji = None
        self._emoji = (
            emojize(self._raw_emoji, variant="emoji_type", language="alias")
            if self._raw_emoji
            else None
        )
        self._validate()

    def _validate(self) -> None:
        if self._value < 0:
            msg = f"Level {self._name} cannot be negative: {self._value}"
            raise NegativeLevelError(msg)
        if not self._color or self._color.isspace():
            msg = f"Level {self._name} has invalid color: {self._color}"
            raise InvalidLevelColorError(msg)
        if self._emoji and not purely_emoji(self._emoji):
            msg = f"Invalid emoji code: {self._raw_emoji}"
            raise InvalidLevelEmojiError(msg)

    def passed_level(self, level: LevelType) -> bool:
        return self.value >= level.value

    def __str__(self) -> str:
        return f"{self.emoji or ''}{self.name}[{self.value}]"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"value={self.value}, "
            f"emoji={self.emoji})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LevelType):
            return self.value == other.value and self.name == other.name
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.value))


class LevelMeta(type):
    _custom_levels: list[LevelType]
    _levels_by_name: dict[str, LevelType]
    _levels_by_value: dict[int, LevelType]
    _custom_levels_lock: Lock
    _standard_levels: tuple[LevelType, ...]

    def __init__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], /, **kwds
    ) -> None:
        super().__init__(name, bases, attrs, **kwds)

        cls._custom_levels: list[LevelType] = []
        cls._custom_levels_lock = Lock()
        cls._standard_levels = tuple(
            level for level in vars(cls).values() if isinstance(level, LevelType)
        )

        cls._levels_by_name = {level.name: level for level in cls._standard_levels}
        cls._levels_by_value = {level.value: level for level in cls._standard_levels}

    def __str__(cls) -> str:
        return (
            f"{cls.__name__}("
            f"standard_levels_count={len(cls._standard_levels)}, "
            f"custom_levels_count={len(cls._custom_levels)})"
        )

    def __repr__(cls) -> str:
        return (
            f"{cls.__name__}("
            f"standard_levels={[str(level) for level in cls.standard_levels()]}, "  # type: ignore[reportAttributeAccessIssue]
            f"custom_levels={[str(level) for level in cls.custom_levels()]})"  # type: ignore[reportAttributeAccessIssue]
        )


class Level(metaclass=LevelMeta):
    NOTSET = LevelType("NOTSET", 0, Fore.RESET, "white_circle")
    VERBOSE = LevelType(
        "VERBOSE", 10, Fore.LIGHTBLACK_EX, "magnifying_glass_tilted_left"
    )
    DEBUG = LevelType("DEBUG", 20, Fore.MAGENTA, "bug")
    TRACE = LevelType("TRACE", 30, Fore.BLUE, "footprints")
    LOG = LevelType("LOG", 40, Fore.CYAN, "page_facing_up")
    NOTICE = LevelType("NOTICE", 50, Fore.LIGHTYELLOW_EX, "loudspeaker")
    EVENT = LevelType("EVENT", 60, Fore.LIGHTCYAN_EX, "bullseye")
    PERFORMANCE = LevelType("PERFORMANCE", 70, Fore.LIGHTMAGENTA_EX, "high_voltage")
    SUCCESS = LevelType("SUCCESS", 80, Fore.GREEN, "check_mark_button")
    SECURITY = LevelType("SECURITY", 90, Fore.LIGHTGREEN_EX, "locked")
    AUDIT = LevelType("AUDIT", 100, Fore.LIGHTYELLOW_EX, "clipboard")
    INFO = LevelType("INFO", 110, Fore.LIGHTBLUE_EX, "information")
    WARNING = LevelType("WARNING", 120, Fore.YELLOW, "warning")
    ERROR = LevelType("ERROR", 130, Fore.LIGHTRED_EX, "cross_mark")
    ALERT = LevelType("ALERT", 140, Style.BRIGHT + Fore.YELLOW, "police_car_light")
    CRITICAL = LevelType("CRITICAL", 150, Style.BRIGHT + Fore.LIGHTRED_EX, "collision")
    FATAL = LevelType("FATAL", 160, Style.BRIGHT + Fore.RED, "skull_and_crossbones")
    EMERGENCY = LevelType("EMERGENCY", 170, Style.BRIGHT + Fore.RED, "ambulance")

    @classmethod
    def get_by_name(cls, name: str) -> LevelType | None:
        try:
            normalized = normalize_level_name(name)
        except InvalidLevelNameError:
            return None
        return cls._levels_by_name.get(normalized, None)

    @classmethod
    def get_by_value(cls, value: int) -> LevelType | None:
        if value < 0:
            return None
        return cls._levels_by_value.get(value, None)

    @classmethod
    def standard_levels(cls) -> list[LevelType]:
        return sorted(
            cls._standard_levels,
            key=lambda level: (level.value, level.name),
        )

    @classmethod
    def custom_levels(cls) -> list[LevelType]:
        return sorted(
            cls._custom_levels,
            key=lambda level: (level.value, level.name),
        )

    @classmethod
    def register(
        cls,
        name: str,
        value: int,
        color: str = Fore.RESET,
        emoji_alias: str | None = None,
    ) -> LevelType:
        normalized = normalize_level_name(name)
        with cls._custom_levels_lock:
            for level in cls._standard_levels:
                if level.name == normalized:
                    msg = f"Level {normalized} is a standard level"
                    raise LevelNameAlreadyExistsError(msg)
                if level.value == value:
                    msg = f"Level value {value} is a standard level"
                    raise LevelValueAlreadyExistsError(msg)

            for level in cls._custom_levels:
                if level.name == normalized:
                    msg = f"Level {normalized} is already registered"
                    raise LevelNameAlreadyExistsError(msg)
                if level.value == value:
                    msg = f"Level value {value} is already registered"
                    raise LevelValueAlreadyExistsError(msg)

            new_level = LevelType(normalized, value, color, emoji_alias)
            cls._custom_levels.append(new_level)
            cls._levels_by_name[new_level.name] = new_level
            cls._levels_by_value[new_level.value] = new_level
            return new_level

    @classmethod
    def unregister(cls, name_or_value: str | int) -> bool:
        with cls._custom_levels_lock:
            level = None
            if isinstance(name_or_value, str):
                level = Level.get_by_name(name_or_value)
            if isinstance(name_or_value, int):
                level = Level.get_by_value(name_or_value)

            if level is not None:
                cls._custom_levels.remove(level)
                del cls._levels_by_name[level.name]
                del cls._levels_by_value[level.value]
                return True
            return False
