from __future__ import annotations

from collections.abc import Callable
from re import Pattern

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Filter

__all__ = ("ContextFilter",)


class ContextFilter(Filter):
    def __init__(
        self,
        *,
        match_all: bool = True,
        **conditions: object | Callable[[object], bool] | Pattern[str],
    ) -> None:
        self.conditions = conditions
        self.check = all if match_all else any

    @staticmethod
    def _check_condition(condition: object, actual: object) -> bool:
        if callable(condition):
            try:
                return condition(actual)  # type: ignore[no-any-return]
            except Exception:  # noqa: BLE001
                return False
        elif isinstance(condition, Pattern):
            return bool(condition.search(str(actual)))  # type: ignore[no-matching-overload]
        else:
            return actual == condition

    def filter(self, record: Record) -> bool:
        context = record.context

        return self.check(
            self._check_condition(condition, context.get(key))
            for key, condition in self.conditions.items()
        )
