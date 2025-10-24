from __future__ import annotations

from typing import Any, Callable, overload


@overload
def pass_exceptions[**P](
    *errors: type[Exception],
) -> Callable[[Callable[P, Any | None]], Callable[P, Any | None]]: ...
@overload
def pass_exceptions[**P, R](
    *errors: type[Exception],
    default: R,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def pass_exceptions(
    *errors: type[Exception],
    default: Any = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type(e) not in errors:
                    raise e from Exception()
            return default

        return wrapper

    return decorator
