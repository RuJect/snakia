from typing import Any, Callable, overload


@overload
def chain[**P, A](func1: Callable[P, A], /) -> Callable[P, A]: ...


@overload
def chain[**P, A, B](
    func1: Callable[P, A], func2: Callable[[A], B], /
) -> Callable[P, B]: ...
@overload
def chain[**P, A, B, C](
    func1: Callable[P, A], func2: Callable[[A], B], func3: Callable[[B], C], /
) -> Callable[P, C]: ...
@overload
def chain[**P, A, B, C, D](
    func1: Callable[P, A],
    func2: Callable[[A], B],
    func3: Callable[[B], C],
    func4: Callable[[C], D],
    /,
) -> Callable[P, D]: ...


@overload
def chain[**P, A, B, C, D, E](
    func1: Callable[P, A],
    func2: Callable[[A], B],
    func3: Callable[[B], C],
    func4: Callable[[C], D],
    func5: Callable[[D], E],
    /,
) -> Callable[P, E]: ...


@overload
def chain[**P, A, B, C, D, E, F](
    func1: Callable[P, A],
    func2: Callable[[A], B],
    func3: Callable[[B], C],
    func4: Callable[[C], D],
    func5: Callable[[D], E],
    func6: Callable[[E], F],
    /,
) -> Callable[P, F]: ...


def chain[**P](
    func1: Callable[P, Any], /, *funcs: Callable[[Any], Any]
) -> Callable[P, Any]:

    def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
        v = func1(*args, **kwargs)
        for f in funcs:
            v = f(v)
        return v

    return inner
