from typing import Any, cast


class PrivProperty[T]:
    def __set_name__(self, owner: type, name: str) -> None:
        self.__name: str = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return cast(T, getattr(instance, self.__name))

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__name, value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__name)

    @property
    def name(self) -> str:
        return self.__name
