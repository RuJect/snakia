from __future__ import annotations

from typing import ClassVar, Self, final, overload

from .os import PlatformOS


class PlatformLayer[T: PlatformOS]:
    target: ClassVar[PlatformOS] = PlatformOS.UNKNOWN

    @final
    def __init__(self, platform: PlatformOS) -> None:
        if platform != self.target:
            raise NotImplementedError(
                f"{self.__class__.__name__} is not implemented for {platform._name_}"
            )

    @overload
    @classmethod
    def try_get(cls, platform: T, /) -> Self: ...
    @overload
    @classmethod
    def try_get(cls, platform: PlatformOS, /) -> Self | None: ...
    @classmethod
    def try_get(cls, platform: PlatformOS, /) -> Self | None:
        if platform == cls.target:
            return cls(platform)
        else:
            return None
