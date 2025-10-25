import operator
from typing import Any, Callable, overload

from snakia.utils import to_async

from .async_bindable import AsyncBindable
from .base_bindable import ValueChanged
from .bindable import Bindable
from .concat import concat


@overload
def combine[T1, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    /,
    *,
    combiner: Callable[[T1], R],
) -> Bindable[R]: ...


@overload
def combine[T1, T2, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    source2: Bindable[T2] | AsyncBindable[T2],
    /,
    *,
    combiner: Callable[[T1, T2], R],
) -> Bindable[R]: ...


@overload
def combine[T1, T2, T3, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    source2: Bindable[T2] | AsyncBindable[T2],
    source3: Bindable[T3] | AsyncBindable[T3],
    /,
    *,
    combiner: Callable[[T1, T2, T3], R],
) -> Bindable[R]: ...


@overload
def combine[T1, T2, T3, T4, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    source2: Bindable[T2] | AsyncBindable[T2],
    source3: Bindable[T3] | AsyncBindable[T3],
    source4: Bindable[T4] | AsyncBindable[T4],
    /,
    *,
    combiner: Callable[[T1, T2, T3, T4], R],
) -> Bindable[R]: ...


@overload
def combine[T1, T2, T3, T4, T5, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    source2: Bindable[T2] | AsyncBindable[T2],
    source3: Bindable[T3] | AsyncBindable[T3],
    source4: Bindable[T4] | AsyncBindable[T4],
    source5: Bindable[T5] | AsyncBindable[T5],
    /,
    *,
    combiner: Callable[[T1, T2, T3, T4, T5], R],
) -> Bindable[R]: ...


@overload
def combine[T1, T2, T3, T4, T5, T6, R](
    source1: Bindable[T1] | AsyncBindable[T1],
    source2: Bindable[T2] | AsyncBindable[T2],
    source3: Bindable[T3] | AsyncBindable[T3],
    source4: Bindable[T4] | AsyncBindable[T4],
    source5: Bindable[T5] | AsyncBindable[T5],
    source6: Bindable[T6] | AsyncBindable[T6],
    /,
    *,
    combiner: Callable[[T1, T2, T3, T4, T5, T6], R],
) -> Bindable[R]: ...


def combine[R](
    *sources: Bindable[Any] | AsyncBindable[Any],
    combiner: Callable[..., R],
) -> Bindable[R]:
    combined = Bindable[R]()
    values = [*map(lambda s: s.value, sources)]

    for i, source in enumerate(sources):

        def make_subscriber(
            index: int,
        ) -> Callable[[ValueChanged[Any]], None]:
            return concat(
                lambda v: operator.setitem(values, index, v.new_value),
                lambda _: combiner(*values),
            )

        if isinstance(source, Bindable):
            source.subscribe(make_subscriber(i))
        else:
            source.subscribe(to_async(make_subscriber(i)))
    return combined
