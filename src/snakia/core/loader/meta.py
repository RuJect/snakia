from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from snakia.core.es import Event, Subscriber
from snakia.types import Version

from .plugin_processor import PluginProcessor


class Meta(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    name: str = Field(
        default="unknown",
        min_length=4,
        max_length=32,
        pattern="^[a-z0-9_]{4,32}$",
    )
    author: str = Field(
        default="unknown",
        min_length=4,
        max_length=32,
        pattern="^[a-z0-9_]{4,32}$",
    )
    version: Version = Field(
        default_factory=lambda: Version(major=1, minor=0, patch=0)
    )

    subscribers: tuple[tuple[type[Event], Subscriber[Event]], ...] = Field(
        default_factory=tuple
    )
    processors: tuple[type[PluginProcessor], ...] = Field(
        default_factory=tuple
    )

    @property
    def id(self) -> str:
        return f"{self.author}.{self.name}"
