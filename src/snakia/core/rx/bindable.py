from typing import Any, Callable

from .value_changed import ValueChanged

type BindableSubscriber[T: Any] = Callable[[ValueChanged[T]], Any]


class Bindable[T: Any]:
    def __init__(self, default_value: T | None = None) -> None:
        self.__subscribers: list[BindableSubscriber[T]] = []
        if default_value is not None:
            self.__default_value: T = default_value
            self.__value: T = default_value

    @property
    def value(self) -> T:
        return self.__value

    @property
    def subscribers(self) -> tuple[BindableSubscriber[T], ...]:
        return (*self.__subscribers,)

    def __call__(self, value: T) -> None:
        self.set(value)

    def set(self, value: T) -> None:
        e = ValueChanged(self.__value, value)
        self.__value = value
        for subscriber in self.__subscribers:
            subscriber(e)

    def subscribe(
        self, subscriber: BindableSubscriber[T], /, run_now: bool = False
    ) -> None:
        self.__subscribers.append(subscriber)
        if run_now:
            subscriber(ValueChanged(self.__default_value, self.value))

    def unsubscribe(self, subscriber: BindableSubscriber[T]) -> None:
        self.__subscribers.remove(subscriber)

    def on(
        self, run_now: bool = False
    ) -> Callable[[BindableSubscriber[T]], None]:
        def wrapper(subscriber: BindableSubscriber[T]) -> None:
            self.subscribe(subscriber, run_now)

        return wrapper
