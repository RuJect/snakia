from typing import override

from .field import Field


class Int(Field[int], type=int):
    @override
    def serialize(self, value: int, /) -> str:
        return str(value)

    @override
    def deserialize(self, serialized: str, /) -> int:
        return int(serialized)

    @override
    def validate(self, serialized: str, /) -> bool:
        return all(c in "1234567890" for c in serialized.removeprefix("-+"))
