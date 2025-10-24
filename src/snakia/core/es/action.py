from __future__ import annotations

from typing import Self

from pydantic import BaseModel, Field


class Action(BaseModel):
    move: int = Field(default=1)

    @classmethod
    def stop(cls) -> Self:
        return cls(move=2**8)

    @classmethod
    def go_start(cls) -> Self:
        return cls(move=-(2**8))

    @classmethod
    def next(cls, count: int = 1) -> Self:
        return cls(move=count)

    @classmethod
    def prev(cls, count: int = 1) -> Self:
        return cls(move=-count)

    @classmethod
    def skip(cls, count: int = 1) -> Self:
        return cls(move=count + 1)
