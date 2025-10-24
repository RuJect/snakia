from __future__ import annotations

import re
from typing import Literal

from snakia.platform import PlatformLayer, PlatformOS


class LinuxLayer(PlatformLayer[Literal[PlatformOS.LINUX]]):
    target = PlatformOS.LINUX

    def os_release_raw(self) -> str:
        try:
            return open("/etc/os-release").read()
        except FileNotFoundError:
            return open("/usr/lib/os-release").read()

    def os_release(self) -> dict[str, str]:
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
        return self.os_release().get("name", "linux")

    def distro_pretty_name(self) -> str:
        return self.os_release().get("PRETTY_NAME", "Linux")

    def distro_id(self) -> str:
        return self.os_release().get("ID", "linux")

    def version(self) -> str:
        return self.os_release().get("VERSION_ID", "0")

    def codename(self) -> str:
        return self.os_release().get("VERSION_CODENAME", "unknown")
