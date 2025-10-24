from collections.abc import Callable
from typing import Any, Self


class classproperty[T]:

    def __init__(
        self,
        fget: Callable[[Any], T] | None = None,
        fset: Callable[[Any, T], None] | None = None,
        fdel: Callable[[Any], None] | None = None,
    ) -> None:
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

    def __get__(self, _: Any, owner: type | None = None, /) -> T:
        if self.__fget is None:
            raise AttributeError("unreadable attribute")
        return self.__fget(owner)

    def __set__(self, instance: Any, value: T, /) -> None:
        if self.__fset is None:
            return
        owner = type(instance) if instance else instance
        return self.__fset(owner, value)

    def __delete__(self, instance: Any, /) -> None:
        if self.__fdel is None:
            return
        owner = type(instance) if instance else instance
        return self.__fdel(owner)

    def getter(self, fget: Callable[[Any], T], /) -> Self:
        self.__fget = fget
        return self

    def setter(self, fset: Callable[[Any, T], None], /) -> Self:
        self.__fset = fset
        return self

    def deleter(self, fdel: Callable[[Any], None], /) -> Self:
        self.__fdel = fdel
        return self
