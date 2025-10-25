from __future__ import annotations

import queue
from collections import defaultdict
from typing import Callable, Final

from snakia.utils import nolock

from .event import Event
from .filter import Filter
from .handler import Handler
from .subscriber import Subscriber


class Dispatcher:
    """
    Event dispatcher
    """

    __running: bool

    def __init__(self) -> None:
        self.__queue: Final = queue.Queue[Event]()
        self.__subscribers: Final[
            dict[type[Event], list[Subscriber[Event]]]
        ] = defaultdict(list)
        self.__running = False

    @property
    def is_running(self) -> bool:
        """Returns True if the dispatcher is running."""
        return self.__running

    def subscribe[T: Event](
        self, event_type: type[T], subscriber: Subscriber[T]
    ) -> None:
        """Subscribe to an event type."""
        self.__subscribers[event_type].append(subscriber)  # type: ignore

    def unsubscribe[T: Event](
        self, event_type: type[T], subscriber: Subscriber[T]
    ) -> None:
        """Unsubscribe from an event type."""
        for sub in self.__subscribers[event_type].copy():
            if sub.handler != subscriber.handler:
                continue
            if sub.priority != subscriber.priority:
                continue
            self.__subscribers[event_type].remove(sub)

    def on[T: Event](
        self,
        event: type[T],
        filter: Filter[T] | None = None,
        priority: int = -1,
    ) -> Callable[[Handler[T]], Handler[T]]:
        """Decorator to subscribe to an event."""

        def wrapper(handler: Handler[T]) -> Handler[T]:
            self.subscribe(event, Subscriber(handler, filter, priority))
            return handler

        return wrapper

    def publish(self, event: Event) -> None:
        """Add an event to the queue."""
        self.__queue.put(event)

    def start(self) -> None:
        """Start the update loop."""
        self.__running = True
        while self.__running:
            self.update()
            nolock()

    def stop(self) -> None:
        """Stop the update loop."""
        self.__running = False

    def update(self, block: bool = False) -> None:
        """Update the dispatcher."""
        try:
            event = self.__queue.get(block=block, timeout=None)
            for base in event.__class__.mro():
                if not issubclass(base, Event):
                    continue
                self.__handle_event(base, event)
            self.__queue.task_done()
        except queue.Empty:
            pass

    def __handle_event(self, event_type: type[Event], event: Event) -> None:
        subscribers = self.__subscribers[event_type]
        subscribers.sort(key=lambda s: s.priority, reverse=True)
        i = 0
        while i < len(subscribers):
            subscriber = subscribers[i]
            if subscriber.filters is not None and not subscriber.filters(
                event
            ):
                continue

            action = subscriber.handler(event)
            if action is not None:
                i = max(0, min(len(subscribers), i + action.move))
            else:
                i += 1
            event.reduce_ttl()
