from __future__ import annotations

from re import IGNORECASE
from re import compile as re_compile
from typing import Any

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Formatter


class SecurityFormatter(Formatter):
    def __init__(
        self,
        inner: Formatter,
        *,
        sensitive_fields: list[str] | None = None,
        sensitive_patterns: list[str] | None = None,
        mask_char: str = "*",
    ) -> None:
        self.inner = inner
        self.sensitive_fields = sensitive_fields or [
            "password",
            "token",
            "secret",
            "api_key",
            "auth",
            "credit_card",
        ]
        self.sensitive_patterns = sensitive_patterns or []
        self._compiled_patterns = [
            re_compile(pattern, IGNORECASE) for pattern in self.sensitive_patterns
        ]
        self.mask_char = mask_char

    def _mask_process(self, item: Any) -> Any:  # noqa: ANN401
        if isinstance(item, list | tuple | set):
            return [self._mask_process(i) for i in item]
        if isinstance(item, dict):
            masked: dict[str, Any] = {}
            for key, value in item.items():
                if not isinstance(key, str):
                    continue
                masked[key] = self._mask_process(value)
            return masked
        if isinstance(item, str) and any(
            pattern.search(item) for pattern in self._compiled_patterns
        ):
            return self.mask_char * len(item)
        return item

    def format(self, record: Record) -> str:
        masked_context = self._mask_process(record.context)

        message = record.message() if callable(record.message) else record.message  # ty:ignore[call-top-callable]
        masked_message = self._mask_process(message)

        new_record = record.copy()
        new_record.context = masked_context
        new_record.message = masked_message

        return self.inner.format(new_record)
