from __future__ import annotations

from itertools import count
from typing import TYPE_CHECKING

from turboprint_logger import Container, get_default_container
from turboprint_logger.core.config import Config
from turboprint_logger.core.levels import LevelType
from turboprint_logger.exceptions.core import LoggerInstantiationError
from turboprint_logger.managers.items import (
    ContextManager,
    FiltersManager,
    HandlersManager,
    ProcessorsManager,
    TagsManager,
)
from turboprint_logger.managers.metrics import MetricsManager
from turboprint_logger.managers.only import FormatterManager, LevelManager
from turboprint_logger.managers.status import StatusManager
from turboprint_logger.utils.normalizers import normalize_logger_name

if TYPE_CHECKING:
    from turboprint_logger.core.logger import Logger

__all__ = ("_LoggerFactory",)

_ROOT_LOGGER_NAME = "root"


class _LoggerFactory:
    _name: str
    _container: Container

    __slots__ = (
        "_container",
        "_logger_id",
        "_name",
        "context",
        "filters",
        "formatter",
        "handlers",
        "level",
        "metrics",
        "parent",
        "processors",
        "propagate",
        "status",
        "tags",
    )

    _logger_counter: count = count()
    _trace_counter: count = count()

    def __init__(self) -> None:
        msg = "Logger cannot be instantiated directly. Use Logger.get_logger()"
        raise LoggerInstantiationError(msg)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def _create(
        cls,
        name: str,
        container: Container,
        config: Config | None = None,
    ) -> Logger:
        config = config or Config()
        self = object.__new__(cls)

        self._logger_id = cls._next_logger_id()
        self._container = container

        if name != _ROOT_LOGGER_NAME:
            parent_name = name.rsplit(".", 1)[0] if "." in name else _ROOT_LOGGER_NAME
            self.parent = cls.get_logger(parent_name, config=None, container=container)
        else:
            self.parent = self  # pyright: ignore[reportAttributeAccessIssue]

        self._name = name
        self.propagate = (
            config.propagate
            if config.propagate is not None
            else container.defaults.propagate
        )
        self._create_managers(config)
        return self  # pyright: ignore[reportReturnType]

    @classmethod
    def get_logger(
        cls,
        name: str = _ROOT_LOGGER_NAME,
        config: Config | None = None,
        container: Container | None = None,
    ) -> Logger:
        _container = container or get_default_container()
        name = normalize_logger_name(name)

        with _container._container_lock:
            if not _container._root_logger:
                _container._root_logger = cls._create(
                    _ROOT_LOGGER_NAME, _container, None
                )

            if name == _ROOT_LOGGER_NAME:
                return _container._root_logger

            existing = _container._loggers.get(name)
            if existing is not None:
                return existing

            effective_config = config or _container._resolve_config_for(name)
            logger = Logger._create(name, _container, effective_config)
            _container._loggers[name] = logger
            return logger

    def _create_managers(self, config: Config) -> None:
        defaults = self._container.defaults

        self.level = LevelManager(
            config.level if config.level is not None else defaults.level.get()
        )
        self.formatter = FormatterManager(
            config.formatter
            if config.formatter is not None
            else defaults.formatter.get()
        )
        self.processors = ProcessorsManager(
            *(
                config.processors
                if config.processors is not None
                else defaults.processors.get()
            )
        )
        self.handlers = HandlersManager(
            *(
                config.handlers
                if config.handlers is not None
                else defaults.handlers.get()
            )
        )
        self.filters = FiltersManager(
            *(config.filters if config.filters is not None else defaults.filters.get())
        )
        self.context = ContextManager(
            **(config.context if config.context is not None else defaults.context.get())
        )
        self.tags = TagsManager(
            *(config.tags if config.tags is not None else defaults.tags.get())
        )
        self.metrics = MetricsManager()

        logger_status = (
            config.status
            if config.status is not None
            else defaults.status.logger.enabled
        )
        self.status = StatusManager(
            logger=logger_status,
            handlers=defaults.status.handlers.enabled,
            filters=defaults.status.filters.enabled,
            global_handlers=defaults.status.global_handlers.enabled,
            global_filters=defaults.status.global_filters.enabled,
        )

    @classmethod
    def _next_logger_id(cls) -> int:
        return next(cls._logger_counter)

    @classmethod
    def _generate_trace_id(cls) -> int:
        return next(cls._trace_counter)

    def is_enabled_for(self, level: LevelType) -> bool:
        if not self.status.logger.enabled:
            return False
        if not level.passed_level(self.level.get()):
            return False
        g = self._container.globals
        if not g.status.logger.enabled:
            return False
        return level.passed_level(g.level.get())
