from __future__ import annotations

from typing import Any, Literal, overload

from pydantic import BaseModel, ConfigDict, Field


class Version(BaseModel):
    model_config = ConfigDict(frozen=True)

    major: int = Field(default=0, ge=0)
    minor: int = Field(default=0, ge=0)
    patch: int = Field(default=0, ge=0)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_compatible(self, other: Version) -> bool:
        return self.major == other.major

    def compare(self, other: Version) -> int:
        """
        - `-1` if self < other
        - `0` if self == other
        - `1` if self > other
        """
        if self.major < other.major:
            return -1
        if self.major > other.major:
            return 1
        if self.minor < other.minor:
            return -1
        if self.minor > other.minor:
            return 1
        if self.patch < other.patch:
            return -1
        if self.patch > other.patch:
            return 1
        return 0

    @overload
    def __gt__(self, other: Version) -> bool: ...

    @overload
    def __gt__(self, other: Any) -> Literal[False]: ...

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) > 0

    @overload
    def __ge__(self, other: Version) -> bool: ...

    @overload
    def __ge__(self, other: Any) -> Literal[False]: ...

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) >= 0

    @overload
    def __lt__(self, other: Version) -> bool: ...

    @overload
    def __lt__(self, other: Any) -> Literal[False]: ...

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) < 0

    @overload
    def __le__(self, other: Version) -> bool: ...

    @overload
    def __le__(self, other: Any) -> Literal[False]: ...

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) <= 0

    @overload
    def __eq__(self, other: Version) -> bool: ...

    @overload
    def __eq__(self, other: Any) -> Literal[False]: ...

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) == 0

    @overload
    def __ne__(self, other: Version) -> bool: ...

    @overload
    def __ne__(self, other: Any) -> Literal[False]: ...

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Version):
            return False
        return self.compare(other) != 0

    @classmethod
    def from_tuple(cls, version: tuple[int, int, int]) -> Version:
        return cls(major=version[0], minor=version[1], patch=version[2])

    @classmethod
    def from_args(cls, major: int, minor: int, patch: int, *_: Any) -> Version:
        return cls(major=major, minor=minor, patch=patch)

    @classmethod
    def from_string(cls, version: str) -> Version:
        return cls.from_args(*map(int, version.split(".")), 0, 0, 0)
