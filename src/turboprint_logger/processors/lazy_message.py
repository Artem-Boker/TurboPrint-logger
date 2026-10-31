from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("LazyMessageProcessor",)


class LazyMessageProcessor(Processor):
    def start(self, record: Record) -> Record:
        message = record.message
        if isinstance(message, str):
            return record

        try:
            record.message = message()
        except Exception as exc:  # noqa: BLE001
            record.context["lazy_message_error"] = exc
            record.message = "<lazy_message_error>"
            return record
        return record
