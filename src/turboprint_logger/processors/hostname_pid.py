from __future__ import annotations

from os import getpid
from socket import gethostname
from threading import get_ident

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("HostnamePidProcessor",)


class HostnamePidProcessor(Processor):
    def process(self, record: Record) -> Record:
        record.context.setdefault("host", gethostname())
        record.context.setdefault("pid", getpid())
        record.context.setdefault("thread_id", get_ident())

        return record
