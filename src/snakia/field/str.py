from typing import override

from .field import Field


class Str(Field[str], type=str):
    @override
    def serialize(self, value: str, /) -> str:
        return value

    @override
    def deserialize(self, serialized: str, /) -> str:
        return serialized

    @override
    def validate(self, serialized: str, /) -> bool:
        return True
