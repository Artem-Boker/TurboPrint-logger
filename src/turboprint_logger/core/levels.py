from __future__ import annotations

from enum import Enum

from colorama import Fore, Style
from emoji import emojize

__all__ = ("Level",)


class Level(Enum):
    NOTSET = (0, Fore.RESET, ":white_circle:")
    VERBOSE = (10, Fore.LIGHTBLACK_EX, ":magnifying_glass_tilted_left:")
    DEBUG = (20, Fore.MAGENTA, ":bug:")
    TRACE = (30, Fore.BLUE, ":detective: ")
    LOG = (40, Fore.CYAN, ":page_facing_up:")
    NOTICE = (50, Fore.LIGHTYELLOW_EX, ":loudspeaker:")
    EVENT = (60, Fore.LIGHTCYAN_EX, ":bullseye:")
    PERFORMANCE = (70, Fore.LIGHTMAGENTA_EX, ":high_voltage:")
    SUCCESS = (80, Fore.GREEN, ":check_mark_button:")
    SECURITY = (90, Fore.LIGHTGREEN_EX, ":locked:")
    AUDIT = (100, Fore.YELLOW, ":eye: ")
    INFO = (110, Fore.LIGHTBLUE_EX, ":information: ")
    WARNING = (120, Fore.YELLOW, ":warning: ")
    ERROR = (130, Fore.LIGHTRED_EX, ":cross_mark:")
    ALERT = (140, Style.BRIGHT + Fore.YELLOW, ":police_car_light:")
    CRITICAL = (150, Style.BRIGHT + Fore.LIGHTRED_EX, ":collision:")
    FATAL = (160, Style.BRIGHT + Fore.RED, ":skull_and_crossbones: ")
    EMERGENCY = (170, Style.BRIGHT + Fore.RED, ":ambulance:")

    _level: int
    _color: str
    _emoji: str | None

    def __init__(self, level: int, color: str, emoji: str | None = None) -> None:
        self._level = level
        self._color = color
        self._emoji = emoji

    @property
    def level(self) -> int:
        return self._level

    @property
    def color(self) -> str:
        return self._color

    @property
    def emoji(self) -> str | None:
        return emojize(self._emoji) if self._emoji else None

    def enabled_for(self, level: Level) -> bool:
        return self.level >= level.level
