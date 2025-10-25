from typing import Any, Callable, Self

from snakia.types import empty


class Property[T]:
    """
    A property that can be set, get, and deleted."""

    def __init__(
        self,
        fget: Callable[[Any], T] = empty.func,
        fset: Callable[[Any, T], None] = empty.func,
        fdel: Callable[[Any], None] = empty.func,
    ) -> None:
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return self.__fget(instance)

    def __set__(self, instance: Any, value: T, /) -> None:
        return self.__fset(instance, value)

    def __delete__(self, instance: Any, /) -> None:
        return self.__fdel(instance)

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
