from typing import Any, Callable, Self

from snakia.types import empty


class classproperty[T]:
    """
    Class property
    """

    __slots__ = ("__fget", "__fset", "__fdel")

    def __init__(
        self,
        fget: Callable[[Any], T],
        fset: Callable[[Any, T], None] = empty.func,
        fdel: Callable[[Any], None] = empty.func,
    ) -> None:
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

    def __get__(self, _: Any, owner: type | None = None, /) -> T:
        return self.__fget(owner)

    def __set__(self, instance: Any | None, value: T, /) -> None:
        owner = type(instance) if instance else instance
        return self.__fset(owner, value)

    def __delete__(self, instance: Any | None, /) -> None:
        owner = type(instance) if instance else instance
        return self.__fdel(owner)

    def getter(self, fget: Callable[[Any], T], /) -> Self:
        """Descriptor getter."""
        self.__fget = fget
        return self

    def setter(self, fset: Callable[[Any, T], None], /) -> Self:
        """Descriptor setter."""
        self.__fset = fset
        return self

    def deleter(self, fdel: Callable[[Any], None], /) -> Self:
        """Descriptor deleter."""
        self.__fdel = fdel
        return self
