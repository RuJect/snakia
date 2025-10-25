from __future__ import annotations

from typing import Self

from pydantic import BaseModel, Field


class Action(BaseModel):
    move: int = Field(default=1)

    @classmethod
    def stop(cls) -> Self:
        """Skip all handlers."""
        return cls(move=2**8)

    @classmethod
    def go_start(cls) -> Self:
        """Go to the first handler."""
        return cls(move=-(2**8))

    @classmethod
    def next(cls, count: int = 1) -> Self:
        """Skip one handler."""
        return cls(move=count)

    @classmethod
    def prev(cls, count: int = 1) -> Self:
        """Go back one handler."""
        return cls(move=-count)

    @classmethod
    def skip(cls, count: int = 1) -> Self:
        """Skip n handlers.

        Args:
            count (int): The number of handlers to skip.
        """
        return cls(move=count + 1)
