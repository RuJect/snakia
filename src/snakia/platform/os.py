from __future__ import annotations

import sys
from enum import IntEnum
from typing import Final


class PlatformOS(IntEnum):
    UNKNOWN = 0b000
    WINDOWS = 0b001
    LINUX = 0b010
    MACOS = 0b011
    IOS = 0b100
    FREEBSD = 0b101
    ANDROID = 0b110

    @property
    def is_apple(self) -> bool:
        return self in [PlatformOS.MACOS, PlatformOS.IOS]

    @property
    def is_linux(self) -> bool:
        return self in [PlatformOS.LINUX, PlatformOS.ANDROID]

    @classmethod
    def resolve(cls) -> PlatformOS:
        if sys.platform in ["win32", "win16", "dos", "cygwin", "msys"]:
            return PlatformOS.WINDOWS
        elif sys.platform.startswith("linux"):
            return PlatformOS.LINUX
        elif sys.platform.startswith("freebsd"):
            return PlatformOS.FREEBSD
        elif sys.platform == "darwin":
            return PlatformOS.MACOS
        elif sys.platform == "ios":
            return PlatformOS.IOS
        elif sys.platform == "android":
            return PlatformOS.ANDROID
        elif sys.platform.startswith("java"):
            return PlatformOS.UNKNOWN
        else:
            return PlatformOS.UNKNOWN


OS: Final[PlatformOS] = PlatformOS.resolve()
