from __future__ import annotations

import re
from typing import Literal

from .layer import PlatformLayer
from .os import PlatformOS


class LinuxLayer(PlatformLayer[Literal[PlatformOS.LINUX]]):
    target = PlatformOS.LINUX

    def os_release_raw(self) -> str:
        """Read /etc/os-release or /usr/lib/os-release"""
        try:
            return open("/etc/os-release", encoding="utf-8").read()
        except FileNotFoundError:
            return open("/usr/lib/os-release", encoding="utf-8").read()

    def os_release(self) -> dict[str, str]:
        """Parse `os_release_raw` and return a dict"""
        raw = self.os_release_raw()
        info = {
            "ID": "linux",
        }
        os_release_line = re.compile(
            "^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>[\"']?)(?P<value>.*)(?P=quote)$"
        )
        os_release_unescape = re.compile(r"\\([\\\$\"\'`])")

        for line in raw.split("\n"):
            mo = os_release_line.match(line)
            if mo is not None:
                info[mo.group("name")] = os_release_unescape.sub(
                    r"\1", mo.group("value")
                )
        return info

    def distro_name(self) -> str:
        """Return the distro name."""
        return self.os_release().get("name", "linux")

    def distro_pretty_name(self) -> str:
        """Return the distro pretty name."""
        return self.os_release().get("PRETTY_NAME", "Linux")

    def distro_id(self) -> str:
        """Return the distro id."""
        return self.os_release().get("ID", "linux")

    def version(self) -> str:
        """Return the distro version."""
        return self.os_release().get("VERSION_ID", "0")

    def codename(self) -> str:
        """Return the distro codename."""
        return self.os_release().get("VERSION_CODENAME", "unknown")
