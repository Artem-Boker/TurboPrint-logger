from __future__ import annotations

from threading import Lock, RLock
from typing import TYPE_CHECKING, ClassVar
from weakref import WeakValueDictionary

from turboprint_logger.core.levels import LevelRegistry
from turboprint_logger.exceptions.core.container import ContainerInstantiationError
from turboprint_logger.managers.collections import DefaultManager, GlobalManager
from turboprint_logger.utils.normalizers import normalize_container_name

if TYPE_CHECKING:
    from turboprint_logger.core.logger import Logger

__all__ = ("Container", "get_default_container")

_DEFAULT_CONTAINER_NAME = "default"


class Container:
    __slots__ = (
        "__weakref__",
        "_container_lock",
        "_loggers",
        "_name",
        "_root_logger",
        "defaults",
        "globals",
    )

    _containers: ClassVar[dict[str, Container]] = {}
    _get_container_lock = Lock()

    def __init__(self) -> None:
        self._container_lock: RLock
        self._root_logger: Logger | None
        self._loggers: WeakValueDictionary[str, Logger]
        self._name: str
        self.globals: GlobalManager
        self.defaults: DefaultManager
        msg = "Container cannot be instantiated directly. Use Container.get_container()"
        raise ContainerInstantiationError(msg)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def _create(cls, name: str = _DEFAULT_CONTAINER_NAME) -> Container:
        self = super().__new__(cls)
        self._container_lock = RLock()
        self._root_logger = None
        self._loggers = WeakValueDictionary()
        self._name = name
        self.globals = GlobalManager()
        self.defaults = DefaultManager()
        return self

    @classmethod
    def get_container(cls, name: str = _DEFAULT_CONTAINER_NAME) -> Container:
        name = normalize_container_name(name)
        with cls._get_container_lock:
            if name == _DEFAULT_CONTAINER_NAME:
                return _DEFAULT_CONTAINER
            if name not in cls._containers:
                container = Container._create(name)
                cls._containers[name] = container
                return container
            return cls._containers[name]

    def get_metrics(self) -> dict[str, dict[LevelRegistry, int]]:
        with self._container_lock:
            loggers = []
            if self._root_logger:
                loggers.append(self._root_logger)
            loggers.extend(self._loggers.values())
        return {logger.name: logger.metrics.items() for logger in loggers}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"loggers={tuple(self._loggers.keys())}, "
            f"globals={self.globals!r}, "
            f"defaults={self.defaults!r})"
        )


_DEFAULT_CONTAINER = Container._create(_DEFAULT_CONTAINER_NAME)


def get_default_container() -> Container:
    return _DEFAULT_CONTAINER
