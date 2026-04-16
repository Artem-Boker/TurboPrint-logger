from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from turboprint_logger.core.levels import LevelRegistry
from turboprint_logger.interfaces import Filter, Formatter, Handler
from turboprint_logger.interfaces.processor import Processor

__all__ = ("Config",)


@dataclass(slots=True)
class Config:
    min_level: LevelRegistry | None = None
    formatter: Formatter | None = None
    processors: list[Processor] | None = None
    handlers: list[Handler] | None = None
    filters: list[Filter] | None = None
    propagate: bool | None = None
    status: bool | None = None
    context: dict[str, Any] | None = None
    tags: set[str] | None = None
