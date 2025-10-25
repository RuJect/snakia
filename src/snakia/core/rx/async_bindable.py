from types import CoroutineType
from typing import Any, Awaitable, Callable, Literal, overload

from .base_bindable import BaseBindable, BindableSubscriber, ValueChanged


class AsyncBindable[T: Any](BaseBindable[T]):
    """
    An asynchronous bindable.
    """

    def __init__(self, default_value: T | None = None) -> None:
        super().__init__(default_value)
        self.__subscribers: list[
            BindableSubscriber[T, CoroutineType[Any, Any, Any]]
        ] = []

    @property
    def value(self) -> T:
        return self.__value

    @property
    def subscribers(
        self,
    ) -> tuple[BindableSubscriber[T, CoroutineType[Any, Any, Any]], ...]:
        """Get the subscribers."""
        return (*self.__subscribers,)

    async def set(self, value: T) -> None:
        """Set the value."""
        e = ValueChanged(self.__value, value)
        self.__value = value
        for subscriber in self.__subscribers:
            await subscriber(e)

    @overload
    def subscribe(
        self,
        subscriber: BindableSubscriber[T, CoroutineType[Any, Any, Any]],
        /,
        run_now: Literal[True],
    ) -> Awaitable[None]: ...

    @overload
    def subscribe(
        self,
        subscriber: BindableSubscriber[T, CoroutineType[Any, Any, Any]],
        /,
        run_now: Literal[False] = False,
    ) -> None: ...

    def subscribe(
        self,
        subscriber: BindableSubscriber[T, CoroutineType[Any, Any, Any]],
        /,
        run_now: bool = False,
    ) -> None | Awaitable[None]:
        """Subscribe to an value."""
        self.__subscribers.append(subscriber)
        if run_now:

            async def _run() -> None:
                await subscriber(
                    ValueChanged(self.__default_value, self.__value)
                )

            return _run()
        return None

    def unsubscribe(
        self, subscriber: BindableSubscriber[T, CoroutineType[Any, Any, Any]]
    ) -> None:
        """Unsubscribe from an value."""
        self.__subscribers.remove(subscriber)

    @overload
    def on(
        self, run_now: Literal[True]
    ) -> Callable[
        [BindableSubscriber[T, CoroutineType[Any, Any, Any]]], Awaitable[None]
    ]: ...

    @overload
    def on(
        self, run_now: Literal[False] = False
    ) -> Callable[
        [BindableSubscriber[T, CoroutineType[Any, Any, Any]]], None
    ]: ...

    def on(self, run_now: bool = False) -> Callable[
        [BindableSubscriber[T, CoroutineType[Any, Any, Any]]],
        None | Awaitable[None],
    ]:
        """Decorator to subscribe to an value."""

        def wrapper(
            subscriber: BindableSubscriber[T, CoroutineType[Any, Any, Any]],
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
