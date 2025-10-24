from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, final

from snakia.utils import inherit


class Field[T: Any](ABC):
    @abstractmethod
    def serialize(self, value: T, /) -> str:
        pass

    @abstractmethod
    def deserialize(self, serialized: str, /) -> T:
        pass

    @abstractmethod
    def validate(self, serialized: str, /) -> bool:
        pass

    @final
    @classmethod
    def custom[R](
        cls: type[Field[Any]],
        serialize: Callable[[R], str],
        deserialize: Callable[[str], R],
    ) -> type[Field[R]]:
        return inherit(
            cls, {"serialize": serialize, "deserialize": deserialize}
        )

    @final
    def __init_subclass__(cls, type: type[T]) -> None:
        setattr(cls, "type", lambda: type)

    if TYPE_CHECKING:

        @classmethod
        def type(cls) -> type[T]: ...
