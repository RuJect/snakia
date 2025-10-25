from typing import Any

from .priv_property import PrivProperty


class initonly[T](PrivProperty[T]):
    def __set__(self, instance: Any, value: T, /) -> None:
        if hasattr(instance, self.name):
            return
        setattr(instance, self.name, value)
