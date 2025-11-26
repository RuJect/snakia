from typing import Any, Awaitable, Callable, TypeVar, overload

from snakia.types import Unset
from snakia.utils import caller, to_async

from .async_bindable import AsyncBindable
from .base_bindable import ValueChanged
from .bindable import Bindable

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
R = TypeVar("R")


@overload
def combine(
    source1: Bindable[A] | AsyncBindable[A],
    /,
    *,
    combiner: Callable[[A], R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


@overload
def combine(
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    /,
    *,
    combiner: Callable[[A, B], R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


@overload
def combine(
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    /,
    *,
    combiner: Callable[[A, B, C], R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


@overload
def combine(
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    source4: Bindable[D] | AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


@overload
def combine(
    source1: Bindable[A] | AsyncBindable[A],
    source2: Bindable[B] | AsyncBindable[B],
    source3: Bindable[C] | AsyncBindable[C],
    source4: Bindable[D] | AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


@overload
def combine(
    *sources: Bindable[Any] | AsyncBindable[Any],
    combiner: Callable[..., R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]: ...


def combine(
    *sources: Bindable[Any] | AsyncBindable[Any],
    combiner: Callable[..., R],
    default_value: R | Unset = Unset(),
) -> Bindable[R]:
    combined = Bindable[R]()
    Unset.map(
        default_value,
        combined.set_silent,
        caller(combined.set_silent, sources[0].default_value),
    )

    def subscriber(_: ValueChanged[Any]) -> None:
        combined.set(combiner(*map(lambda s: s.value, sources)))

    for source in sources:
        if isinstance(source, Bindable):
            source.subscribe(subscriber)
        else:
            source.subscribe(to_async(subscriber))
    return combined


@overload
def async_combine(
    source1: AsyncBindable[A],
    /,
    *,
    combiner: Callable[[A], Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


@overload
def async_combine(
    source1: AsyncBindable[A],
    source2: AsyncBindable[B],
    /,
    *,
    combiner: Callable[[A, B], Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


@overload
def async_combine(
    source1: AsyncBindable[A],
    source2: AsyncBindable[B],
    source3: AsyncBindable[C],
    /,
    *,
    combiner: Callable[[A, B, C], Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


@overload
def async_combine(
    source1: AsyncBindable[A],
    source2: AsyncBindable[B],
    source3: AsyncBindable[C],
    source4: AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


@overload
def async_combine(
    source1: AsyncBindable[A],
    source2: AsyncBindable[B],
    source3: AsyncBindable[C],
    source4: AsyncBindable[D],
    /,
    *,
    combiner: Callable[[A, B, C, D], Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


@overload
def async_combine(
    *sources: AsyncBindable[Any],
    combiner: Callable[..., Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]: ...


def async_combine(
    *sources: AsyncBindable[Any],
    combiner: Callable[..., Awaitable[R]],
    default_value: R | Unset = Unset(),
) -> AsyncBindable[R]:
    combined = AsyncBindable[R]()
    Unset.map(
        default_value,
        combined.set_silent,
        caller(combined.set_silent, sources[0].default_value),
    )

    async def subscriber(_: ValueChanged[Any]) -> None:
        result = await combiner(*map(lambda s: s.value, sources))
        await combined.set(result)

    for source in sources:
        source.subscribe(subscriber)
    return combined
