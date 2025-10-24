from typing import override

from .field import Field


class Float(Field[float], type=int):
    @override
    def serialize(self, value: float, /) -> str:
        return str(value)

    @override
    def deserialize(self, serialized: str, /) -> float:
        return float(serialized)

    @override
    def validate(self, serialized: str, /) -> bool:
        serialized = serialized.removeprefix("-+")
        if serialized.count(".") > 1:
            return False
        return all(c in "1234567890." for c in serialized)
