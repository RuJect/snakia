from typing import Any, Callable, TypeGuard, TypeVar, final

T = TypeVar("T")
V = TypeVar("V")
R = TypeVar("R")


@final
class UniqueType(type):
    """
    A metaclass that prevents multiple instances of a class from being created.
    """

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ) -> type:
        t = super().__new__(mcs, name, bases, {})
        setattr(t, "__new__", lambda cls, *args, **kwargs: cls)
        return t

    @final
    def __init__(
        cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> None:
        super().__init__(name, bases, namespace)

    def __instancecheck__(cls, instance: Any) -> bool:
        return instance is cls

    def __eq__(cls, other: Any) -> bool:
        return cls is other

    def __call__(cls: type[T]) -> T:
        return cls.__new__(cls)  # noqa: E1120 # pylint: disable=E1120

    def __hash__(cls) -> int:
        return id(cls)

    def itis(cls: type[T], value: Any) -> TypeGuard[T]:
        return value is cls or isinstance(value, cls)

    def unwrap(cls: type[T], value: V | type[T] | T, /) -> V:
        if value is cls or isinstance(value, cls):
            raise TypeError(f"{cls} not unwrapped")
        return value  # type: ignore

    def unwrap_or(cls: type[T], value: V | type[T] | T, default: R, /) -> V | R:
        if value is cls or isinstance(value, cls):
            return default
        return value  # type: ignore

    def map(
        cls: type[T],
        value: V | type[T] | T,
        or_else: Callable[[V], R],
        and_then: Callable[[type[T]], R],
    ) -> R:
        if value is cls or isinstance(value, cls):
            return and_then(cls)
        return or_else(value)  # type: ignore

    def or_else(
        cls: type[T], value: V | type[T] | T, func: Callable[[V], R]
    ) -> type[T] | R:
        if value is cls or isinstance(value, cls):
            return cls
        return func(value)  # type: ignore

    def and_then(
        cls: type[T], value: V | type[T] | T, func: Callable[[type[T]], R]
    ) -> R | V:
        if value is cls or isinstance(value, cls):
            return func(cls)
        return value  # type: ignore


class Unique(metaclass=UniqueType):  # noqa: R0903 # pylint: disable=R0903
    """
    A class that prevents multiple instances of a class from being created.
    """


def unique(name: str) -> UniqueType:
    """Factory for creating a unique type."""
    return UniqueType(name, (), {})
