from __future__ import annotations

from typing import Any, Protocol, TypeVar


class FunctionLike(Protocol):
    """Decorated function: a callable object that also has a name."""

    __name__: str

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...  # noqa: ANN401


FuncT = TypeVar("FuncT", bound=FunctionLike)
