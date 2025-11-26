from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    TypeVar,
    final,
)

from snakia.property.priv_property import PrivProperty
from snakia.utils import inherit

T = TypeVar("T")
R = TypeVar("R")


class Field(ABC, PrivProperty[T], Generic[T]):
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
    def custom(
        cls: type[Field[Any]],
        serialize: Callable[[Field[R], R], bytes],
        deserialize: Callable[[Field[R], bytes], R],
    ) -> type[Field[R]]:
        return inherit(
            cls, {"serialize": serialize, "deserialize": deserialize}
        )

    @final
    @staticmethod
    def get_fields(class_: type[Any] | Any, /) -> dict[str, Field[Any]]:
        if not isinstance(class_, type):
            class_ = class_.__class__
        return {
            k: v for k, v in class_.__dict__.items() if isinstance(v, Field)
        }

    if TYPE_CHECKING:

        @final
        @classmethod
        def type(cls) -> type[T]: ...
