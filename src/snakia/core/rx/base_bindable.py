from typing import Generic, Protocol, TypeVar

from typing_extensions import NamedTuple

T = TypeVar("T")
R_co = TypeVar("R_co", covariant=True)


class ValueChanged(NamedTuple, Generic[T]):
    old_value: T
    new_value: T


class BindableSubscriber(Protocol, Generic[T, R_co]):
    def __call__(self, value: ValueChanged[T], /) -> R_co: ...


class BaseBindable(Generic[T]):
    def __init__(self, default_value: T | None = None) -> None:
        if default_value is not None:
            self.__default_value: T = default_value
            self.__value: T = default_value

    @property
    def default_value(self) -> T:
        return self.__default_value

    @property
    def value(self) -> T:
        if self.has_value:
            return self.__value
        return self.default_value

    @property
    def has_value(self) -> bool:
        try:
            _ = self.__value
            return True
        except AttributeError:
            return False

    @property
    def has_default_value(self) -> bool:
        try:
            _ = self.__default_value
            return True
        except AttributeError:
            return False

    def set_silent(self, value: T) -> None:
        self.__value = value
