from typing import Any, cast


class PrivProperty[T]:
    __slots__ = ("__name",)

    __name: str

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return cast(T, getattr(instance, self.__name))

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__name, value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__name)

    @property
    def name(self) -> str:
        """Return the name of the variable associated with the property."""
        return self.__name
