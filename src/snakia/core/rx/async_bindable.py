from typing import Any, Awaitable, Callable, Literal, cast, overload

from .value_changed import ValueChanged

type AsyncBindableSubscriber[T: Any] = Callable[
    [ValueChanged[T]], Awaitable[Any]
]


class AsyncBindable[T: Any]:
    def __init__(self, default_value: T | None = None) -> None:
        self.__subscribers: list[AsyncBindableSubscriber[T]] = []
        if default_value is not None:
            self.__default_value: T = default_value
            self.__value: T = default_value

    @property
    def value(self) -> T:
        return self.__value

    @property
    def subscribers(self) -> tuple[AsyncBindableSubscriber[T], ...]:
        return (*self.__subscribers,)

    async def __call__(self, value: T) -> None:
        await self.set(value)

    async def set(self, value: T) -> None:
        e = ValueChanged(self.__value, value)
        self.__value = value
        for subscriber in self.__subscribers:
            await subscriber(e)

    @overload
    def subscribe(
        self,
        subscriber: AsyncBindableSubscriber[T],
        /,
        run_now: Literal[True],
    ) -> Awaitable[None]: ...

    @overload
    def subscribe(
        self,
        subscriber: AsyncBindableSubscriber[T],
        /,
        run_now: Literal[False] = False,
    ) -> None: ...

    def subscribe(
        self, subscriber: AsyncBindableSubscriber[T], /, run_now: bool = False
    ) -> None | Awaitable[None]:
        self.__subscribers.append(subscriber)
        if run_now:

            async def _run() -> None:
                await subscriber(
                    ValueChanged(self.__default_value, self.__value)
                )

            return _run()
        return None

    def unsubscribe(self, subscriber: AsyncBindableSubscriber[T]) -> None:
        self.__subscribers.remove(subscriber)

    @overload
    def on(
        self, run_now: Literal[True]
    ) -> Callable[[AsyncBindableSubscriber[T]], Awaitable[None]]: ...

    @overload
    def on(
        self, run_now: Literal[False] = False
    ) -> Callable[[AsyncBindableSubscriber[T]], None]: ...

    def on(
        self, run_now: bool = False
    ) -> Callable[[AsyncBindableSubscriber[T]], None | Awaitable[None]]:
        def wrapper(
            subscriber: AsyncBindableSubscriber[T],
        ) -> None | Awaitable[None]:
            self.__subscribers.append(subscriber)
            if run_now:

                async def _run() -> None:
                    await subscriber(
                        ValueChanged(self.__default_value, self.__value)
                    )

                return _run()
            return None

        return wrapper
