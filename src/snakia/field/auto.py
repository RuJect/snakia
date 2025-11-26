import pickle
from typing import Callable, Final, Generic, TypeVar, overload

from typing_extensions import Self

from snakia.types import Unset

from .field import Field

T = TypeVar("T")


class AutoField(Field[T], Generic[T]):
    __slots__ = ("__target_type",)

    @overload
    def __init__(
        self, default_value: T, *, target_type: type[T] | Unset = Unset()
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        default_factory: Callable[[Self], T],
        target_type: type[T] | Unset = Unset(),
    ) -> None: ...

    def __init__(
        self,
        default_value: T | Unset = Unset(),
        *,
        default_factory: Callable[[Self], T] | Unset = Unset(),
        target_type: type[T] | Unset = Unset(),
    ) -> None:
        if not Unset.itis(default_factory):
            super().__init__(default_factory=Unset.unwrap(default_factory))
        elif not Unset.itis(default_value):
            super().__init__(Unset.unwrap(default_value))
        else:
            super().__init__()
        self.__target_type: Final[type] = Unset.unwrap_or(target_type, object)

    def serialize(self, value: T, /) -> bytes:
        return pickle.dumps(value)

    def deserialize(self, serialized: bytes, /) -> T:
        value = pickle.loads(serialized)
        
        if not isinstance(value, self.__target_type):
            return self._get_default()
        return value  # type: ignore
