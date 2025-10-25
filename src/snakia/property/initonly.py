from typing import Any

from .priv_property import PrivProperty


class Initonly[T](PrivProperty[T]):
    """Property that can only be set once."""

    def __set__(self, instance: Any, value: T, /) -> None:
        if hasattr(instance, self.name):
            return
        super().__set__(instance, value)


def initonly() -> Initonly[Any]:
    """Factory for `Initonly`."""
    return Initonly()
