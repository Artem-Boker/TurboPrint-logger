from __future__ import annotations

from os import getpid
from socket import gethostname
from threading import get_ident

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("HostnamePidProcessor",)


class HostnamePidProcessor(Processor):
    def __init__(self) -> None:
        self._hostname = gethostname()
        self._pid = getpid()

    def process(self, record: Record) -> Record:
        record.context.setdefault("host", self._hostname)
        record.context.setdefault("pid", self._pid)
        record.context.setdefault("thread_id", get_ident())

        return record
