from typing import Any, Callable, Final, Generic, TypeVar, overload

from typing_extensions import Self

from snakia.types import Unset

T = TypeVar("T")


class PrivProperty(Generic[T]):
    __slots__ = "__name", "__default_value", "__default_factory"

    __name: str

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, default_value: T) -> None: ...
    @overload
    def __init__(self, *, default_factory: Callable[[Self], T]) -> None: ...
    def __init__(
        self,
        default_value: T | Unset = Unset(),
        default_factory: Callable[[Self], T] | Unset = Unset(),
    ) -> None:
        self.__default_value: Final[T | Unset] = default_value
        self.__default_factory: Final[Callable[[Self], T] | Unset] = default_factory

    def _get_default(self: Self) -> T:
        return Unset.map(
            self.__default_factory,
            lambda f: f(self),
            lambda _: Unset.unwrap(self.__default_value),
        )

    def __set_name__(self, owner: type, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: Any, owner: type | None = None, /) -> T:
        if not hasattr(instance, self.__name):
            setattr(instance, self.__name, self._get_default())
        return getattr(instance, self.__name)  # type: ignore

    def __set__(self, instance: Any, value: T, /) -> None:
        setattr(instance, self.__name, value)

    def __delete__(self, instance: Any, /) -> None:
        delattr(instance, self.__name)

    @property
    def name(self) -> str:
        """Return the name of the variable associated with the property."""
        return self.__name
