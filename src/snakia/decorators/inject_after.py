from typing import Callable

from .inject_replace import inject_replace


def inject_after[T: object, **P, R](
    obj: T, target: Callable[P, R], hook: Callable[[R], R]
) -> T:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return hook(target(*args, **kwargs))

    return inject_replace(obj, target, inner)


def after_hook[**P, R](
    obj: object, target: Callable[P, R]
) -> Callable[[Callable[[R], R]], Callable[[R], R]]:
    def hook(new: Callable[[R], R]) -> Callable[[R], R]:
        inject_after(obj, target, new)
        return new

    return hook
