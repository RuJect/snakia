from typing import Any, Callable


def concat[**P](*funcs: Callable[P, Any]) -> Callable[P, None]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> None:
        for f in funcs:
            f(*args, **kwargs)

    return inner
