from typing import Any, Callable

from .base_bindable import BaseBindable, BindableSubscriber, ValueChanged


class Bindable[T: Any](BaseBindable[T]):
    """
    A bindable value.
    """

    def __init__(self, default_value: T | None = None) -> None:
        super().__init__(default_value)
        self.__subscribers: list[BindableSubscriber[T, Any]] = []

    @property
    def subscribers(self) -> tuple[BindableSubscriber[T, Any], ...]:
        """Get the subscribers."""
        return (*self.__subscribers,)

    def set(self, value: T) -> None:
        """Set the value."""
        e = ValueChanged(self.__value, value)
        self.set_silent(value)
        for subscriber in self.__subscribers:
            subscriber(e)

    def subscribe(
        self, subscriber: BindableSubscriber[T, Any], /, run_now: bool = False
    ) -> None:
        """Subscribe to an value."""
        self.__subscribers.append(subscriber)
        if run_now:
            subscriber(ValueChanged(self.default_value, self.value))

    def unsubscribe(self, subscriber: BindableSubscriber[T, Any]) -> None:
        """Unsubscribe from an value."""
        self.__subscribers.remove(subscriber)

    def on(
        self, run_now: bool = False
    ) -> Callable[[BindableSubscriber[T, Any]], None]:
        """Decorator to subscribe to an value."""

        def wrapper(subscriber: BindableSubscriber[T, Any]) -> None:
            self.subscribe(subscriber, run_now)

        return wrapper
