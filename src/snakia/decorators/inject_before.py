from typing import Any, Callable

from .inject_replace import inject_replace


def inject_before[T: object, **P, R](
    obj: T, target: Callable[P, R], hook: Callable[P, Any]
) -> T:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        hook(*args, **kwargs)
        return target(*args, **kwargs)

    return inject_replace(obj, target, inner)


def before_hook[**P, R](
    obj: object, target: Callable[P, R]
) -> Callable[[Callable[P, Any]], Callable[P, Any]]:

    def hook(new: Callable[P, Any]) -> Callable[P, Any]:
        inject_before(obj, target, new)
        return new

    return hook
