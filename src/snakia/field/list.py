from typing import Callable, Final, Iterable, TypeVar

from typing_extensions import Self

from .field import Field

T = TypeVar("T")


class ListField(Field[list[T]]):
    def __init__(
        self,
        field: Field[T],
        *,
        length_size: int = 1,
        default_factory: Callable[[Self], Iterable[T]] = lambda _: (),
    ) -> None:
        self.length_size: Final[int] = length_size
        self.field: Final = field
        super().__init__(default_factory=lambda s: [*default_factory(s)])

    def serialize(self, items: list[T], /) -> bytes:
        result = b""
        for item in items:
            value = self.field.serialize(item)
            length_prefix = len(value).to_bytes(self.length_size, "big")
            result += length_prefix + value
        return result

    def deserialize(self, serialized: bytes, /) -> list[T]:
        result = []
        while serialized:
            length = int.from_bytes(serialized[: self.length_size], "big")
            serialized = serialized[self.length_size :]
            item = self.field.deserialize(serialized[:length])
            serialized = serialized[length:]
            result.append(item)
        return result
