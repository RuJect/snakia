from __future__ import annotations

from typing import Protocol

from .event import Event


class Filter[T: Event](Protocol):
    """Filter for an event."""

    def __call__(self, event: T) -> bool: ...
