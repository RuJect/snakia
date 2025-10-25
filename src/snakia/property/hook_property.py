from typing import Any, Callable, Self

from snakia.types import empty

from .priv_property import PrivProperty


class HookProperty[T](PrivProperty[T]):
    """
    A property that calls a function when the property is set, get, or deleted.
    """

    __slots__ = ("__on_set", "__on_get", "__on_del")

    def __init__(
        self,
        on_set: Callable[[T], None],
        on_get: Callable[[T], None] = empty.func,
        on_del: Callable[[T], None] = empty.func,
    ) -> None:
        self.__on_set: Callable[[T], None] = on_set
        self.__on_get: Callable[[T], None] = on_get
        self.__on_del: Callable[[T], None] = on_del

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        value = super().__get__(instance, owner)
        self.__on_get(value)
        return value

    def __set__(self, instance: Any, value: T, /) -> None:
        self.__on_set(value)
        return super().__set__(instance, value)

    def __delete__(self, instance: Any, /) -> None:
        value = super().__get__(instance)
        self.__on_del(value)
        return super().__delete__(instance)

    def getter(self, on_get: Callable[[T], None], /) -> Self:
        """Descriptor getter."""
        self.__on_get = on_get
        return self

    def setter(self, on_set: Callable[[T], None], /) -> Self:
        """Descriptor setter."""
        self.__on_set = on_set
        return self

    def deleter(self, on_del: Callable[[T], None], /) -> Self:
        """Descriptor deleter."""
        self.__on_del = on_del
        return self
