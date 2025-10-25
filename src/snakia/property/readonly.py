from typing import Any, Callable


class Readonly[T]:

    def __init__(
        self,
        fget: Callable[[Any], T],
    ) -> None:
        self.__fget = fget

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        return self.__fget(instance)

    def __set__(self, instance: Any, value: T, /) -> None:
        pass


def readonly[T](value: T) -> Readonly[T]:
    return Readonly(lambda _: value)
