from typing import Callable


def const[T](value: T) -> Callable[[], T]:
    return lambda: value
