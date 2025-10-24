from typing import Final, override

from .field import Field


class Bool(Field[bool], type=bool):
    TRUE_VALUES: Final = ("true", "yes", "y", "+", "1")
    FALSE_VALUES: Final = ("false", "no", "n", "-", "0")

    @override
    def serialize(self, value: bool, /) -> str:
        return str(value)

    @override
    def deserialize(self, serialized: str, /) -> bool:
        return serialized.lower() not in Bool.FALSE_VALUES

    @override
    def validate(self, serialized: str, /) -> bool:
        return serialized.lower() in (*Bool.FALSE_VALUES, *Bool.TRUE_VALUES)
