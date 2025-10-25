from typing import Callable


def inject_replace[T: object, **P, R](
    obj: T, old: Callable[P, R], new: Callable[P, R]
) -> T:
    for k, v in obj.__dict__.items():
        if v is old:
            setattr(obj, k, new)
    return obj


def replace_hook[**P, R](
    obj: object, old: Callable[P, R]
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def hook(new: Callable[P, R]) -> Callable[P, R]:
        inject_replace(obj, old, new)
        return new

    return hook
