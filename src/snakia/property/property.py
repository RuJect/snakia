from collections.abc import Callable
from typing import Any, Self


class Property[T]:

    def __init__(
        self,
        fget: Callable[[Any], T] | None = None,
        fset: Callable[[Any, T], None] | None = None,
        fdel: Callable[[Any], None] | None = None,
    ) -> None:
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        if self.__fget is None:
            raise AttributeError("unreadable attribute")
        return self.__fget(instance)

    def __set__(self, instance: Any, value: T, /) -> None:
        if self.__fset is None:
            return
        return self.__fset(instance, value)

    def __delete__(self, instance: Any, /) -> None:
        if self.__fdel is None:
            return
        return self.__fdel(instance)

    def getter(self, fget: Callable[[Any], T], /) -> Self:
        self.__fget = fget
        return self

    def setter(self, fset: Callable[[Any, T], None], /) -> Self:
        self.__fset = fset
        return self

    def deleter(self, fdel: Callable[[Any], None], /) -> Self:
        self.__fdel = fdel
        return self
