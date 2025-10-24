from typing import Awaitable, Callable


def to_async[**P, R](func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return inner
