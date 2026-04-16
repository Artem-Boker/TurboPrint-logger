from __future__ import annotations

from typing import Any, ClassVar

from colorama import Fore, Style
from emoji import emojize, is_emoji

from turboprint_logger.exceptions.core.levels import (
    InvalidLevelColorError,
    InvalidLevelEmojiError,
    LevelNameAlreadyExistsError,
    LevelValueAlreadyExistsError,
    NegativeLevelError,
)
from turboprint_logger.utils.normalizers import normalize_level_name

__all__ = ("Level", "LevelRegistry")


class LevelRegistry:
    __slots__ = ("_color", "_emoji", "_name", "_value")

    _name: str
    _value: int
    _color: str
    _emoji: str | None

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
        return (
            emojize(self._emoji, variant="emoji_type", language="alias")
            if self._emoji
            else None
        )

    def __init__(
        self, name: str, value: int, color: str, alias_emoji_code: str | None = None
    ) -> None:
        self._name = normalize_level_name(name)
        self._value = value
        self._color = color
        self._emoji = alias_emoji_code.lower() if alias_emoji_code else alias_emoji_code
        self.__post_init__()

    def __post_init__(self) -> None:
        if self._value < 0:
            msg = f"Level {self._name} cannot be negative: {self._value}"
            raise NegativeLevelError(msg)
        if not self._color or self._color.isspace():
            msg = f"Level {self._name} has invalid color: {self._color}"
            raise InvalidLevelColorError(msg)
        if self._emoji and not is_emoji(emojize(self._emoji, language="alias").strip()):
            msg = f"Invalid emoji code: {self._emoji}"
            raise InvalidLevelEmojiError(msg)

    def __str__(self) -> str:
        return f"{self.emoji or ''}{self.name}[{self.value}]"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"value={self.value}, "
            f"emoji={self.emoji})"
        )

    def enabled_for(self, level: LevelRegistry) -> bool:
        return self.value >= level.value


class LevelMeta(type):
    def __init__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], /, **kwds
    ) -> None:
        super().__init__(name, bases, attrs, **kwds)

        cls._standard_levels = tuple(
            level for level in vars(cls).values() if isinstance(level, LevelRegistry)
        )

    def __str__(cls) -> str:
        return cls.__str__()

    def __repr__(cls) -> str:
        return cls.__repr__()


class Level(metaclass=LevelMeta):
    NOTSET = LevelRegistry("NOTSET", 0, Fore.RESET, ":white_circle:")
    VERBOSE = LevelRegistry(
        "VERBOSE", 10, Fore.LIGHTBLACK_EX, ":magnifying_glass_tilted_left:"
    )
    DEBUG = LevelRegistry("DEBUG", 20, Fore.MAGENTA, ":bug:")
    TRACE = LevelRegistry("TRACE", 30, Fore.BLUE, ":detective: ")
    LOG = LevelRegistry("LOG", 40, Fore.CYAN, ":page_facing_up:")
    NOTICE = LevelRegistry("NOTICE", 50, Fore.LIGHTYELLOW_EX, ":loudspeaker:")
    EVENT = LevelRegistry("EVENT", 60, Fore.LIGHTCYAN_EX, ":bullseye:")
    PERFORMANCE = LevelRegistry(
        "PERFORMANCE", 70, Fore.LIGHTMAGENTA_EX, ":high_voltage:"
    )
    SUCCESS = LevelRegistry("SUCCESS", 80, Fore.GREEN, ":check_mark_button:")
    SECURITY = LevelRegistry("SECURITY", 90, Fore.LIGHTGREEN_EX, ":locked:")
    AUDIT = LevelRegistry("AUDIT", 100, Fore.YELLOW, ":eye: ")
    INFO = LevelRegistry("INFO", 110, Fore.LIGHTBLUE_EX, ":information: ")
    WARNING = LevelRegistry("WARNING", 120, Fore.YELLOW, ":warning: ")
    ERROR = LevelRegistry("ERROR", 130, Fore.LIGHTRED_EX, ":cross_mark:")
    ALERT = LevelRegistry(
        "ALERT", 140, Style.BRIGHT + Fore.YELLOW, ":police_car_light:"
    )
    CRITICAL = LevelRegistry(
        "CRITICAL", 150, Style.BRIGHT + Fore.LIGHTRED_EX, ":collision:"
    )
    FATAL = LevelRegistry(
        "FATAL", 160, Style.BRIGHT + Fore.RED, ":skull_and_crossbones: "
    )
    EMERGENCY = LevelRegistry("EMERGENCY", 170, Style.BRIGHT + Fore.RED, ":ambulance:")

    _standard_levels: tuple[LevelRegistry, ...]
    _custom_levels: ClassVar[list[LevelRegistry]] = []

    @classmethod
    def get_by_name(cls, name: str) -> LevelRegistry | None:
        name = normalize_level_name(name)
        for level in cls._standard_levels:
            if level.name == name:
                return level
        for level in cls._custom_levels:
            if level.name == name:
                return level
        return None

    @classmethod
    def get_by_level(cls, value: int) -> LevelRegistry | None:
        if value < 0:
            return None
        for level in cls._standard_levels:
            if level.value == value:
                return level
        for level in cls._custom_levels:
            if level.value == value:
                return level
        return None

    @classmethod
    def standard_levels(cls) -> list[LevelRegistry]:
        return sorted(
            cls._standard_levels,
            key=lambda level: (level.value, level.name),
        )

    @classmethod
    def custom_levels(cls) -> list[LevelRegistry]:
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
    ) -> LevelRegistry:
        for level in cls._standard_levels:
            if level.name == name:
                msg = f"Level {name} is a standard level"
                raise LevelNameAlreadyExistsError(msg)
            if level.value == value:
                msg = f"Level value {value} is a standard level"
                raise LevelValueAlreadyExistsError(msg)

        for level in cls._custom_levels:
            if level.name == name:
                msg = f"Level {name} is already registered"
                raise LevelNameAlreadyExistsError(msg)
            if level.value == value:
                msg = f"Level value {value} is already registered"
                raise LevelValueAlreadyExistsError(msg)

        new_level = LevelRegistry(name, value, color, emoji_alias)
        cls._custom_levels.append(new_level)
        return new_level

    @classmethod
    def unregister(cls, name_or_value: str | int) -> bool:
        for level in cls._custom_levels:
            if name_or_value in (level.name, level.value):
                cls._custom_levels.remove(level)
                return True
        return False

    @classmethod
    def __str__(cls) -> str:
        return f"{cls.__name__}(standard_levels_count={len(cls._standard_levels)}, custom_levels_count={len(cls._custom_levels)})"  # noqa: E501

    @classmethod
    def __repr__(cls) -> str:
        return f"{cls.__name__}(standard_levels={[str(level) for level in cls.standard_levels()]}, custom_levels={[str(level) for level in cls.custom_levels()]})"  # noqa: E501
