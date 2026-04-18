from __future__ import annotations

from queue import Queue

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Processor

__all__ = ("QueueProcessor",)


class QueueProcessor(Processor):
    __slots__ = ("_block", "_queue", "_timeout")

    def __init__(
        self,
        queue: Queue[Record] | None = None,
        *,
        block: bool = True,
        timeout: float | None = None,
    ) -> None:
        self._queue = queue or Queue()
        self._block = block
        self._timeout = timeout

    def start(self, record: Record) -> Record | None:
        try:  # noqa: SIM105
            self._queue.put(record, block=self._block, timeout=self._timeout)
        except Exception:  # noqa: BLE001, S110
            pass
        return record

    @property
    def queue(self) -> Queue[Record]:
        return self._queue

    def get(
        self, block: bool = True, timeout: float | None = None  # noqa: FBT001, FBT002
    ) -> Record:
        return self._queue.get(block=block, timeout=timeout)

    def task_done(self) -> None:
        self._queue.task_done()

    def join(self) -> None:
        self._queue.join()
