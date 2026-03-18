from __future__ import annotations

from turboprint_logger import filters, formatters, handlers
from turboprint_logger.core.plugins import (
    register_filter,
    register_formatter,
    register_handler,
)


def _register_from_package(package, registry_func) -> None:  # noqa: ANN001
    if not hasattr(package, "__all__"):
        return
    for name in package.__all__:
        cls = getattr(package, name)
        registry_func(name)(cls)


def register_all(
    *,
    filters_enabled: bool = True,
    formatters_enabled: bool = True,
    handlers_enabled: bool = True,
) -> None:
    if filters_enabled:
        _register_from_package(filters, register_filter)
    if formatters_enabled:
        _register_from_package(formatters, register_formatter)
    if handlers_enabled:
        _register_from_package(handlers, register_handler)
