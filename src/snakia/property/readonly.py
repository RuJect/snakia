from typing import Any, Callable


class Readonly[T]:
    """
    Readonly property.
    """

    __slots__ = ("__fget",)

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
    """Create a readonly property with the given value.

    Args:
        value (T): The value to set the readonly property to.

    Returns:
        Readonly[T]: The readonly property.
    """
    return Readonly(lambda _: value)
