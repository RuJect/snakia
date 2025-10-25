from typing import Awaitable, Callable


def to_async[**P, R](func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """Convert a sync function to an async function."""

    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return inner
