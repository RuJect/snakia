from typing import Final, override

from .field import Field


class StrField(Field[str]):
    def __init__(self, default_value: str, *, encoding: str = "utf-8") -> None:
        super().__init__(default_value)
        self.encoding: Final = encoding

    @override
    def serialize(self, value: str, /) -> bytes:
        return value.encode(self.encoding)

    @override
    def deserialize(self, serialized: bytes, /) -> str:
        return serialized.decode(self.encoding)
