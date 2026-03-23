from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from turboprint_logger.core.levels import LevelRegistry
from turboprint_logger.interfaces import Filter, Formatter, Handler

__all__ = ("Config",)


@dataclass(slots=True)
class Config:
    min_level: LevelRegistry | None = None
    formatter: Formatter | None = None
    handlers: list[Handler] | None = None
    filters: list[Filter] | None = None
    propagate: bool | None = None
    metrics: dict[LevelRegistry, int] | None = None
    status: bool | None = None
    context: dict[str, Any] | None = None
    tags: set[str] | None = None
