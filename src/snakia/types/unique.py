from typing import Any, final


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

    def __call__[T](cls: type[T]) -> T:
        return cls.__new__(cls)


class Unique(metaclass=UniqueType):
    """
    A class that prevents multiple instances of a class from being created.
    """


def unique(name: str) -> UniqueType:
    """Factory for creating a unique type."""
    return UniqueType(name, (), {})
