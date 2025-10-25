from typing import Any, Callable, Self

from .priv_property import PrivProperty

type _Cell[T] = T | None
type _Getter[T] = Callable[[Any, _Cell[T]], T]
type _Setter[T] = Callable[[Any, _Cell[T], T], _Cell[T]]
type _Deleter[T] = Callable[[Any, _Cell[T]], _Cell[T]]


class CellProperty[T](PrivProperty[T]):

    def __init__(
        self,
        fget: _Getter[T] | None = None,
        fset: _Setter[T] | None = None,
        fdel: _Deleter[T] | None = None,
    ) -> None:
        self.__fget: _Getter[T] | None = fget
        self.__fset: _Setter[T] | None = fset
        self.__fdel: _Deleter[T] | None = fdel

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        if self.__fget is None:
            raise AttributeError("unreadable attribute")
        cell = self.__fget(instance, self.__get_cell(instance))
        self.__set_cell(instance, cell)
        return cell

    def __set__(self, instance: Any, value: T, /) -> None:
        if self.__fset is None:
            return
        cell = self.__fset(instance, self.__get_cell(instance), value)
        self.__set_cell(instance, cell)

    def __delete__(self, instance: Any, /) -> None:
        if self.__fdel is None:
            return
        cell = self.__fdel(instance, self.__get_cell(instance))
        self.__set_cell(instance, cell)

    def getter(self, fget: _Getter[T], /) -> Self:
        self.__fget = fget
        return self

    def setter(self, fset: _Setter[T], /) -> Self:
        self.__fset = fset
        return self

    def deleter(self, fdel: _Deleter[T], /) -> Self:
        self.__fdel = fdel
        return self

    def __get_cell(self, instance: Any) -> T | None:
        return getattr(instance, self.name, None)

    def __set_cell(self, instance: Any, value: T | None) -> None:
        if value is None:
            delattr(instance, self.name)
        else:
            setattr(instance, self.name, value)
