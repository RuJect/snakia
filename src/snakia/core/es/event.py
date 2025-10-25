from __future__ import annotations

from abc import ABC

from pydantic import BaseModel, Field


class Event(ABC, BaseModel):
    ttl: int = Field(default=2**6, kw_only=True, ge=0)

    def reduce_ttl(self) -> None:
        """Reduce the TTL of the event by 1."""
        self.ttl -= 1
