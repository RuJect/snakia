from .async_bindable import AsyncBindable
from .bindable import Bindable


def merge[T](
    *sources: Bindable[T],
) -> Bindable[T]:
    merged = Bindable[T]()
    for source in sources:
        source.subscribe(lambda v: merged.set(v.new_value), run_now=True)
    return merged


async def async_merge[T](
    *sources: AsyncBindable[T],
) -> AsyncBindable[T]:
    merged = AsyncBindable[T]()
    for source in sources:
        await source.subscribe(lambda v: merged.set(v.new_value), run_now=True)
    return merged
