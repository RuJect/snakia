from typing import override

from .field import Field


class BoolField(Field[bool]):
    @override
    def serialize(self, value: bool, /) -> bytes:
        return b"\x01" if value else b"\x00"

    @override
    def deserialize(self, serialized: bytes, /) -> bool:
        return serialized == b"\x01"
