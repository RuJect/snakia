import struct
from typing import override

from .field import Field


class FloatField(Field[float]):
    @override
    def serialize(self, value: float, /) -> bytes:
        return struct.pack(">f", value)

    @override
    def deserialize(self, serialized: bytes, /) -> float:
        return struct.unpack(">f", serialized)[0]  # type: ignore
