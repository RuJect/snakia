import builtins
from typing import Any, Callable, Iterable


def map[T: Any, U](
    func: Callable[[T], U], /
) -> Callable[[Iterable[T]], Iterable[U]]:
    return lambda iterable: builtins.map(func, iterable)
