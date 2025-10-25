from typing import Any


def inherit[T: type](
    type_: T, attrs: dict[str, Any] | None = None, **kwargs: Any
) -> T:
    return type("", (type_,), attrs or {}, **kwargs) # type: ignore
