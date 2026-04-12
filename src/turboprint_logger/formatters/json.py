from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from turboprint_logger.core.record import Record
from turboprint_logger.interfaces import Formatter

JSON_MODULE = "json"
try:
    import orjson

    JSON_MODULE = "orjson"
except ImportError:
    try:
        from msgspec.json import Encoder

        JSON_MODULE = "msgspec"
    except ImportError:
        try:
            from ujson import dumps
        except ImportError:
            from json import dumps

__all__ = ("JSONFormatter",)


class JSONFormatter(Formatter):
    def __init__(
        self,
        *,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
        rename: dict[str, str] | None = None,
        sort_keys: bool = False,
        **extra,
    ) -> None:
        self.include = set(include) if include else None
        self.exclude = set(exclude) if exclude else None
        self.rename = rename or {}
        self.extra = extra or {}
        self.sort_keys = sort_keys

        if JSON_MODULE == "msgspec":
            order = "sorted" if sort_keys else "deterministic"
            self._encoder = Encoder(enc_hook=self._default_serializer, order=order)
        elif JSON_MODULE == "orjson":
            self._orjson_option = orjson.OPT_SERIALIZE_NUMPY
            if sort_keys:
                self._orjson_option |= orjson.OPT_SORT_KEYS

    @staticmethod
    def _default_serializer(obj: Any) -> Any:  # noqa: ANN401, PLR0911
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        for method_name in ("dict", "to_dict","__json__","__dict__"):
            method_obj = getattr(obj, method_name, None)
            if callable(method_obj):
                return method_obj
        return str(obj)

    def format(self, record: Record) -> str:
        message = record.message() if callable(record.message) else record.message  # ty:ignore[call-top-callable]

        data: dict[str, Any] = {
            "message": message,
            "level": {
                "name": record.level.name,
                "value": record.level.level,
            },
            "logger": record.logger.name,
            "timestamp": record.date_time.isoformat(),
            "caller": {
                "file": record.file,
                "function": record.function,
                "line": record.line,
            },
            "context": self._default_serializer({**record.context, **self.extra}),
        }

        for old, new in self.rename.items():
            if old in data:
                data[new] = data.pop(old)

        if self.exclude:
            data = {
                key: value for key, value in data.items() if key not in self.exclude
            }

        if self.include:
            data = {key: value for key, value in data.items() if key in self.include}

        if JSON_MODULE == "orjson":
            return orjson.dumps(
                data, default=self._default_serializer, option=self._orjson_option
            ).decode("utf-8")
        if JSON_MODULE == "msgspec":
            return self._encoder.encode(data).decode("utf-8")
        return dumps(
            data,
            ensure_ascii=False,
            default=self._default_serializer,
            sort_keys=self.sort_keys,
        )
