from typing import Any

__all__ = ("filter_reserved",)

_RESERVED_KEYS = ("level", "message", "tags")


def filter_reserved(extra: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in extra.items() if key not in _RESERVED_KEYS}
