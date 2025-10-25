from typing import Any, NamedTuple, Protocol


class ValueChanged[T](NamedTuple):
    old_value: T
    new_value: T


class BindableSubscriber[T: Any, R: Any](Protocol):
    def __call__(self, value: ValueChanged[T]) -> R: ...


class BaseBindable[T: Any]:
    def __init__(self, default_value: T | None = None) -> None:
        if default_value is not None:
            self.__default_value: T = default_value
            self.__value: T = default_value

    @property
    def default_value(self) -> T:
        return self.__default_value

    @property
    def value(self) -> T:
        return self.__value

    def set_silent(self, value: T) -> None:
        self.__value = value
