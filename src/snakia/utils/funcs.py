from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def call(f: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return f(*args, **kwargs)


def caller(f: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Callable[..., T]:
    return lambda *_, **__: f(*args, **kwargs)


def side(value: T, *_: Any, **__: Any) -> T:
    return value


def side_func(value: T, *_: Any, **__: Any) -> Callable[..., T]:
    return lambda *_, **__: value


def ret() -> Callable[[T], T]:
    return lambda x: x
