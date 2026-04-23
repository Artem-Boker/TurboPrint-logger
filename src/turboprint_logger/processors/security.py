from __future__ import annotations

from re import IGNORECASE
from re import compile as re_compile
from typing import Any

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("SecurityProcessor",)
_DEFAULT_FIELD_PATTERNS = [
    r"api_key$",
    r"api_secret$",
    r"access_token$",
    r"refresh_token$",
    r"client_secret$",
    r"client_id$",
    r"password$",
    r"secret$",
    r"token$",
]


class SecurityProcessor(Processor):
    def __init__(
        self,
        sensitive_patterns: list[str] | None = None,
        mask_char: str = "*",
    ) -> None:
        self._compiled_patterns = [
            re_compile(pattern.strip().lower(), IGNORECASE)
            for pattern in sensitive_patterns or _DEFAULT_FIELD_PATTERNS
        ]
        self.mask_char = mask_char

    def _mask_process(self, item: Any) -> Any:  # noqa: ANN401
        if isinstance(item, (list, tuple, set, frozenset)):
            return type(item)([self._mask_process(i) for i in item])
        if isinstance(item, dict):
            masked: dict[str, Any] = {}
            for key, value in item.items():
                stripped_key = key.strip()
                if any(
                    pattern.search(stripped_key) for pattern in self._compiled_patterns
                ):
                    masked[stripped_key] = self.mask_char * len(str(value))
                else:
                    masked[stripped_key] = self._mask_process(value)
            return masked
        if isinstance(item, str):
            stripped = item.strip()
            if any(pattern.search(stripped) for pattern in self._compiled_patterns):
                return self.mask_char * len(stripped)
            return stripped
        return item

    def start(self, record: Record) -> Record:
        masked_context = self._mask_process(record.context)
        masked_tags = self._mask_process(record.tags)

        message = (
            record.message()  # ty:ignore[call-top-callable]
            if callable(record.message)
            else record.message
        )
        masked_message = self._mask_process(message)

        record.context = masked_context
        record.tags = masked_tags
        record.message = masked_message

        return record
