from __future__ import annotations

from collections.abc import Callable
from json import loads as json_loads
from pathlib import Path
from sys import stderr
from threading import Event, RLock, Thread
from time import sleep
from typing import TYPE_CHECKING, Any, Protocol, TypeAlias, cast

from turboprint_logger.core.levels import Level, LevelRegistry
from turboprint_logger.core.plugins import (
    get_filter,
    get_formatter,
    get_handler,
    get_processor,
)
from turboprint_logger.exceptions.managers.config import (
    ConfigParserError,
    ConfigReloadError,
    ConfigSpecError,
    ConfigWatchAlreadyRunningError,
)
from turboprint_logger.interfaces import Filter, Formatter, Handler
from turboprint_logger.interfaces.processor import Processor

if TYPE_CHECKING:
    from turboprint_logger.core.container import Container
    from turboprint_logger.core.logger import Logger

__all__ = ("ConfigManager",)

_ROOT_LOGGER_NAME = "root"
_MAX_CONFIG_BYTES = 10 * 1024 * 1024


class ParserFunc(Protocol):
    def __call__(self, source: str) -> dict[str, Any]: ...


ComponentFactory: TypeAlias = Callable[[dict[str, Any]], object]


class ConfigManager:
    __slots__ = (
        "_container",
        "_factories",
        "_last_loaded",
        "_lock",
        "_parsers",
        "_stop_event",
        "_watch_file",
        "_watch_interval",
        "_watch_thread",
    )

    def __init__(self, container: Container | None = None) -> None:
        from turboprint_logger.core.container import (  # noqa: PLC0415
            get_default_container,
        )

        self._container = container or get_default_container()
        self._lock = RLock()
        self._parsers: dict[str, ParserFunc] = {}
        self._factories: dict[str, ComponentFactory] = {}
        self._last_loaded: dict[str, Any] | None = None
        self._watch_file: Path | None = None
        self._watch_interval = 1.0
        self._watch_thread: Thread | None = None
        self._stop_event = Event()
        self.register_parser("json", self._parse_json)
        self.register_parser("yaml", self._parse_yaml)
        self.register_parser("yml", self._parse_yaml)
        self._register_default_factories()

    def register_parser(self, extension: str, parser: ParserFunc) -> None:
        key = extension.strip().lower().removeprefix(".")
        with self._lock:
            self._parsers[key] = parser

    def register_factory(self, name: str, factory: ComponentFactory) -> None:
        key = name.strip().lower()
        with self._lock:
            self._factories[key] = factory

    def parse_file(self, file_path: str | Path) -> dict[str, Any]:
        path = Path(file_path).expanduser()
        if not path.is_file():
            msg = f"Config file does not exist or is not a file: {path}"
            raise ConfigParserError(msg)
        suffix = path.suffix.strip().lower().removeprefix(".")
        with self._lock:
            parser = self._parsers.get(suffix)
        if not parser:
            msg = f"Unsupported config extension: {path.suffix or '<none>'}"
            raise ConfigParserError(msg)
        try:
            size = path.stat().st_size
            if size > _MAX_CONFIG_BYTES:
                msg = (
                    f"Config file {path} is too large: {size} bytes. "
                    f"Maximum allowed is {_MAX_CONFIG_BYTES} bytes"
                )
                raise ConfigParserError(msg)
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            msg = f"Unable to read config file {path}: {exc}"
            raise ConfigParserError(msg) from exc
        except UnicodeDecodeError as exc:
            msg = f"Config file {path} is not valid UTF-8: {exc}"
            raise ConfigParserError(msg) from exc
        try:
            data = parser(source)
        except ConfigParserError:
            raise
        except Exception as exc:
            msg = f"Failed to parse config file {path}: {exc}"
            raise ConfigParserError(msg) from exc
        if not isinstance(data, dict):
            msg = "Config root must be an object/dict"
            raise ConfigSpecError(msg)
        return data

    def load_file(self, file_path: str | Path) -> dict[str, Any]:
        config = self.parse_file(file_path)
        self.apply(config)
        with self._lock:
            self._last_loaded = config
        return config

    def apply(self, config: dict[str, Any]) -> None:
        from turboprint_logger.core.logger import Logger  # noqa: PLC0415

        loggers = cast(dict[str, Any], config.get("loggers", {}))
        if not isinstance(loggers, dict):
            msg = "Config key 'loggers' must be a dict"
            raise ConfigSpecError(msg)
        for name, raw_spec in loggers.items():
            if not isinstance(name, str):
                msg = f"Logger name must be a string, got: {type(name).__name__}"
                raise ConfigSpecError(msg)
            if not isinstance(raw_spec, dict):
                msg = f"Logger config for '{name}' must be a dict"
                raise ConfigSpecError(msg)
            logger_name = _ROOT_LOGGER_NAME if name == _ROOT_LOGGER_NAME else name

            logger = Logger.get_logger(logger_name, container=self._container)
            self._apply_logger(logger, raw_spec)

    def enable_auto_reload(
        self,
        file_path: str | Path,
        *,
        interval: float = 1.0,
        load_initial: bool = True,
    ) -> None:
        path = Path(file_path)
        if interval <= 0:
            msg = "Auto-reload interval must be > 0"
            raise ConfigReloadError(msg)

        with self._lock:
            if self._watch_thread and self._watch_thread.is_alive():
                msg = "Auto-reload already enabled"
                raise ConfigWatchAlreadyRunningError(msg)
            self._watch_file = path
            self._watch_interval = interval
            self._stop_event.clear()
            self._watch_thread = Thread(target=self._watch_loop, daemon=True)
            thread = self._watch_thread

        if load_initial:
            try:
                self.load_file(path)
            except Exception:
                with self._lock:
                    self._watch_file = None
                    self._watch_thread = None
                    self._stop_event.set()
                raise

        if thread:
            thread.start()

    def disable_auto_reload(self, *, timeout: float = 2.0) -> None:
        with self._lock:
            thread = self._watch_thread
            self._watch_thread = None
            self._watch_file = None
            self._stop_event.set()
        if thread:
            thread.join(timeout=timeout)

    def is_auto_reload_enabled(self) -> bool:
        with self._lock:
            return bool(self._watch_thread and self._watch_thread.is_alive())

    def _watch_loop(self) -> None:
        last_signature: tuple[int, int] | None = None
        while not self._stop_event.is_set():
            with self._lock:
                path = self._watch_file
                interval = self._watch_interval
            if path is None:
                return

            try:
                stat = path.stat()
                signature = (int(stat.st_mtime_ns), stat.st_size)
            except OSError:
                sleep(interval)
                continue

            if last_signature is None:
                last_signature = signature
            elif signature != last_signature:
                try:
                    self.load_file(path)
                except Exception as exc:  # noqa: BLE001
                    stderr.write(
                        f"{exc.__class__.__name__}[ConfigManager]: "
                        f"Auto-reload failed for {path}: {exc}\n"
                    )
                else:
                    last_signature = signature
            sleep(interval)

    def _register_default_factories(self) -> None:
        self.register_factory("formatter", self._build_formatter)
        self.register_factory("filter", self._build_filter)
        self.register_factory("handler", self._build_handler)
        self.register_factory("processor", self._build_processor)

    def _apply_logger(self, logger: Logger, spec: dict[str, Any]) -> None:
        if "min_level" in spec:
            logger.level.set(self._as_level(spec["min_level"]))

        if "formatter" in spec:
            formatter = cast(
                Formatter, self._build_component("formatter", spec["formatter"])
            )
            logger.formatter.set(formatter)

        if "handlers" in spec:
            handlers_spec = spec["handlers"]
            if not isinstance(handlers_spec, list):
                msg = "Logger key 'handlers' must be a list"
                raise ConfigSpecError(msg)
            handlers = [
                cast(Handler, self._build_component("handler", item))
                for item in handlers_spec
            ]
            logger.handlers.clear()
            logger.handlers.add(*handlers)

        if "processors" in spec:
            processors_spec = spec["processors"]
            if not isinstance(processors_spec, list):
                msg = "Logger key 'processors' must be a list"
                raise ConfigSpecError(msg)
            processors = [
                cast(Processor, self._build_component("processor", item))
                for item in processors_spec
            ]
            logger.processors.clear()
            logger.processors.add(*processors)

        if "filters" in spec:
            filters_spec = spec["filters"]
            if not isinstance(filters_spec, list):
                msg = "Logger key 'filters' must be a list"
                raise ConfigSpecError(msg)
            filters = [
                cast("Filter", self._build_component("filter", item))
                for item in filters_spec
            ]
            logger.filters.clear()
            logger.filters.add(*filters)

        if "propagate" in spec:
            logger.propagate = bool(spec["propagate"])

        if "status" in spec:
            logger.status.logger.set(bool(spec["status"]))

        if "context" in spec:
            context = spec["context"]
            if not isinstance(context, dict):
                msg = "Logger key 'context' must be a dict"
                raise ConfigSpecError(msg)
            logger.context.clear()
            logger.context.update(**context)

        if "tags" in spec:
            tags = spec["tags"]
            if not isinstance(tags, list):
                msg = "Logger key 'tags' must be a list"
                raise ConfigSpecError(msg)
            logger.tags.clear()
            logger.tags.add(*[str(tag) for tag in tags])

    def _build_component(self, kind: str, spec: str | dict[str, Any]) -> object:
        with self._lock:
            factory = self._factories.get(kind)
        if not factory:
            msg = f"Unknown component kind '{kind}'"
            raise ConfigSpecError(msg)

        normalized_spec: dict[str, Any]
        if isinstance(spec, str):
            normalized_spec = {"name": spec}
        elif isinstance(spec, dict):
            normalized_spec = dict(spec)
        else:
            msg = f"Invalid {kind} spec: {spec!r}"
            raise ConfigSpecError(msg)

        return factory(normalized_spec)

    @staticmethod
    def _parse_json(source: str) -> dict[str, Any]:
        payload = json_loads(source)
        if not isinstance(payload, dict):
            msg = "JSON config root must be an object"
            raise ConfigParserError(msg)
        return payload

    @staticmethod
    def _parse_yaml(source: str) -> dict[str, Any]:
        try:
            from yaml import safe_load  # noqa: PLC0415
        except ImportError as exc:
            msg = (
                "YAML parser is unavailable. Install 'PyYAML' to load .yaml/.yml files"
            )
            raise ConfigParserError(msg) from exc
        payload = safe_load(source)
        if payload is None:
            return {}
        if not isinstance(payload, dict):
            msg = "YAML config root must be an object"
            raise ConfigParserError(msg)
        return payload

    @staticmethod
    def _as_level(value: object) -> LevelRegistry:
        if isinstance(value, LevelRegistry):
            return value
        if isinstance(value, str):
            level = Level.get_by_name(value)
            if level:
                return level
        msg = f"Unknown level: {value!r}"
        raise ConfigSpecError(msg)

    def _build_formatter(self, spec: dict[str, Any]) -> Formatter:
        name = str(spec.get("name", "")).strip()
        kwargs = spec.get("kwargs", {})
        if not name:
            msg = "Formatter spec requires non-empty 'name'"
            raise ConfigSpecError(msg)
        if not isinstance(kwargs, dict):
            msg = "Formatter 'kwargs' must be a dict"
            raise ConfigSpecError(msg)
        try:
            cls = get_formatter(name)
            return cls(**kwargs)
        except Exception as exc:
            msg = f"Unable to build formatter '{name}': {exc}"
            raise ConfigSpecError(msg) from exc

    def _build_filter(self, spec: dict[str, Any]) -> Filter:
        name = str(spec.get("name", "")).strip()
        kwargs = spec.get("kwargs", {})
        if not name:
            msg = "Filter spec requires non-empty 'name'"
            raise ConfigSpecError(msg)
        if not isinstance(kwargs, dict):
            msg = "Filter 'kwargs' must be a dict"
            raise ConfigSpecError(msg)

        kwargs = dict(kwargs)
        if "min_level" in kwargs:
            kwargs["min_level"] = self._as_level(kwargs["min_level"])
        if "max_level" in kwargs:
            kwargs["max_level"] = self._as_level(kwargs["max_level"])
        if "allowed_levels" in kwargs and isinstance(kwargs["allowed_levels"], list):
            kwargs["allowed_levels"] = [
                self._as_level(item) for item in kwargs["allowed_levels"]
            ]

        try:
            cls = get_filter(name)
            return cls(**kwargs)
        except Exception as exc:
            msg = f"Unable to build filter '{name}': {exc}"
            raise ConfigSpecError(msg) from exc

    def _build_processor(self, spec: dict[str, Any]) -> Processor:
        name = str(spec.get("name", "")).strip()
        kwargs = spec.get("kwargs", {})
        if not name:
            msg = "Processor spec requires non-empty 'name'"
            raise ConfigSpecError(msg)
        if not isinstance(kwargs, dict):
            msg = "Processor 'kwargs' must be a dict"
            raise ConfigSpecError(msg)

        try:
            cls = get_processor(name)
            return cls(**kwargs)
        except Exception as exc:
            msg = f"Unable to build processor '{name}': {exc}"
            raise ConfigSpecError(msg) from exc

    def _build_handler(self, spec: dict[str, Any]) -> Handler:
        name = str(spec.get("name", "")).strip()
        kwargs = spec.get("kwargs", {})
        if not name:
            msg = "Handler spec requires non-empty 'name'"
            raise ConfigSpecError(msg)
        if not isinstance(kwargs, dict):
            msg = "Handler 'kwargs' must be a dict"
            raise ConfigSpecError(msg)

        kwargs = dict(kwargs)
        if "min_level" in kwargs:
            kwargs["min_level"] = self._as_level(kwargs["min_level"])
        if "formatter" in kwargs:
            kwargs["formatter"] = self._build_component(
                "formatter", kwargs["formatter"]
            )
        if "filters" in kwargs:
            if not isinstance(kwargs["filters"], list):
                msg = "Handler key 'filters' must be a list"
                raise ConfigSpecError(msg)
            kwargs["filters"] = [
                self._build_component("filter", filter_spec)
                for filter_spec in kwargs["filters"]
            ]

        try:
            cls = get_handler(name)
            return cls(**kwargs)
        except Exception as exc:
            msg = f"Unable to build handler '{name}': {exc}"
            raise ConfigSpecError(msg) from exc
