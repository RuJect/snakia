from typing import Final, TypeVar

from .field import Field

T = TypeVar("T")


class OptionalField(Field[T | None]):

    def __init__(
        self,
        field: Field[T],
        *,
        none_value: bytes = b"",
    ) -> None:
        super().__init__(None)
        self.none_value: Final = none_value
        self.field: Final = field

    def serialize(self, value: T | None, /) -> bytes:
        if value is None:
            return self.none_value
        return self.field.serialize(value)

    def deserialize(self, serialized: bytes, /) -> T | None:
        if serialized == self.none_value:
            return None
        return self.field.deserialize(serialized)
