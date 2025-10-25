from typing import Any, final


@final
class UniqueType(type):
    """
    A metaclass that prevents multiple instances of a class from being created.
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ) -> type:
        t = super().__new__(cls, name, bases, {})
        setattr(t, "__new__", lambda cls, *args, **kwargs: cls)
        return t

    @final
    def __init__(
        self, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> None:
        super().__init__(name, bases, namespace)

    def __instancecheck__(self, instance: Any) -> bool:
        return instance is self

    def __eq__(self, other: Any) -> bool:
        return self is other

    def __call__[T](self: type[T]) -> T:
        return self.__new__(self)


class Unique(metaclass=UniqueType):
    """
    A class that prevents multiple instances of a class from being created.
    """


def unique(name: str) -> UniqueType:
    """Factory for creating a unique type."""
    return UniqueType(name, (), {})
