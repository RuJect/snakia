import sys
from types import FunctionType
from typing import Any, Callable, cast

if sys.version_info >= (3, 13):

    def inject_const[T: Callable[..., Any]](**consts: Any) -> Callable[[T], T]:
        def inner(func: T) -> T:
            values = [*func.__code__.co_consts]
            for i, name in enumerate(func.__code__.co_varnames):
                if name in consts:
                    values[i + 1] = consts[name]
            return cast(
                T,
                FunctionType(
                    code=func.__code__.replace(co_consts=(*values,)),
                    globals=func.__globals__,
                    name=func.__name__,
                    argdefs=func.__defaults__,
                    closure=func.__closure__,
                    kwdefaults=func.__kwdefaults__,
                ),
            )

        return inner

else:

    def inject_const[T: Callable[..., Any]](**consts: Any) -> Callable[[T], T]:
        def inner(func: T) -> T:
            values = [*func.__code__.co_consts]
            for i, name in enumerate(func.__code__.co_varnames):
                if name in consts:
                    values[i + 1] = consts[name]
            return cast(
                T,
                FunctionType(
                    code=func.__code__.replace(co_consts=(*values,)),
                    globals=func.__globals__,
                    name=func.__name__,
                    argdefs=func.__defaults__,
                    closure=func.__closure__,
                    # kwdefaults=func.__kwdefaults__,
                ),
            )

        return inner
