from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Final, final

from snakia.utils import inherit


class Field[T: Any](ABC):
    def __init__(self, default_value: T) -> None:
        self.default_value: Final[T] = default_value

    @abstractmethod
    def serialize(self, value: T, /) -> bytes:
        """Serialize a value

        :param value: value to serialize
        :type value: T
        :return: serialized value
        :rtype: bytes
        """

    @abstractmethod
    def deserialize(self, serialized: bytes, /) -> T:
        """Deserialize a value

        :param serialized: serialized value
        :type serialized: bytes
        :return: deserialized value
        :rtype: T
        """

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

    if TYPE_CHECKING:

        @classmethod
        def type(cls) -> type[T]: ...
