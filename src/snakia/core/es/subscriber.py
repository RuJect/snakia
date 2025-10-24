from __future__ import annotations

from typing import NamedTuple

from .event import Event
from .filter import Filter
from .handler import Handler


class Subscriber[T: Event](NamedTuple):
    handler: Handler[T]
    filters: Filter[T] | None
    priority: int
