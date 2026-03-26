from __future__ import annotations

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("LazyMessageProcessor",)


class LazyMessageProcessor(Processor):
    def process(self, record: Record) -> Record:
        if not callable(record.message):
            return record

        try:
            record.message = record.message()  # ty:ignore[call-top-callable]
        except Exception as exc:  # noqa: BLE001
            record.context["lazy_message_error"] = exc
            record.message = "<lazy_message_error>"
            return record
        return record
