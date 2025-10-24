from typing import Any, cast


def inherit[T: type](
    type_: T, attrs: dict[str, Any] | None = None, **kwargs: Any
) -> T:
    return cast(T, type("", (type_,), attrs or {}, **kwargs))
