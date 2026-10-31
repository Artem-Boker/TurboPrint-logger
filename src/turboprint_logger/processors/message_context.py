from __future__ import annotations

from string import Template

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("MessageContextProcessor",)


class MessageContextProcessor(Processor):
    def __init__(self, **context) -> None:
        self.context = context

    def start(self, record: Record) -> Record:
        message = record.resolve_message()
        record.message = Template(message).safe_substitute(
            {**record.context, **self.context}
        )
        return record
