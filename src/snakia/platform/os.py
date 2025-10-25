from __future__ import annotations

import sys
from enum import IntEnum
from typing import Final


class PlatformOS(IntEnum):
    UNKNOWN = 0
    ANDROID = 1
    FREEBSD = 2
    IOS = 3
    LINUX = 4
    MACOS = 5
    WINDOWS = 6

    @property
    def is_apple(self) -> bool:
        """MacOS, iOS"""
        return self in [PlatformOS.MACOS, PlatformOS.IOS]

    @property
    def is_linux(self) -> bool:
        """Linux, Android"""
        return self in [PlatformOS.LINUX, PlatformOS.ANDROID]

    @classmethod
    def resolve(cls) -> PlatformOS:
        """Get the current platform."""
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
"""The current platform."""
