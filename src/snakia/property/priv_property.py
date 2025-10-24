from typing import Any, cast


class PrivProperty[T]:

    def __init__(
        self,
        name: str,
    ) -> None:
        self.__name = name

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return cast(T, getattr(instance, self.__get_name(instance)))

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__get_name(instance), value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__get_name(instance))

    def __get_name(
        self,
        instance: Any,
    ) -> str:
        return f"_priv{instance.__class__.__name__}__{self.__name}"
