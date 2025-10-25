from typing import override

from .field import Field


class IntField(Field[int]):
    @override
    def serialize(self, value: int, /) -> bytes:
        length = (value.bit_length() + 7) // 8
        return value.to_bytes(length, "little")

    @override
    def deserialize(self, serialized: bytes, /) -> int:
        return int.from_bytes(serialized, "little")
