from __future__ import annotations

from ctypes import CDLL, Array, c_char, c_char_p, create_string_buffer
from typing import Any, Literal, cast, overload

from snakia.platform import PlatformLayer, PlatformOS


class AndroidLayer(PlatformLayer[Literal[PlatformOS.ANDROID]]):
    target = PlatformOS.ANDROID

    @overload
    def get_prop(self, name: str) -> str | None: ...
    @overload
    def get_prop[T](self, name: str, default: T) -> str | T: ...
    def get_prop(self, name: str, default: Any = None) -> Any:
        PROP_VALUE_MAX = 92
        buffer = create_string_buffer(PROP_VALUE_MAX)
        length = self.system_property_get(name.encode("UTF-8"), buffer)
        if length == 0:
            return default
        else:
            return buffer.value.decode("UTF-8", "backslashreplace")

    def system_property_get(self, name: bytes, default: Array[c_char]) -> int:
        func = getattr(CDLL("libc.so"), "__system_property_get")
        func.argtypes = (c_char_p, c_char_p)
        result = cast(int, func(name, default))
        return result

    def release(self, default: str = "") -> str:
        return self.get_prop("ro.build.version.release", default)

    def api_level(self, default: int) -> int:
        return int(self.get_prop("ro.build.version.sdk", default))

    def manufacturer(self, default: str = "") -> str:
        return self.get_prop("ro.product.manufacturer", default)

    def model(self, default: str = "") -> str:
        return self.get_prop("ro.product.model", default)

    def device(self, default: str = "") -> str:
        return self.get_prop("ro.product.device", default)

    def is_emulator(self, default: bool) -> bool:
        prop = self.get_prop("ro.kernel.qemu", None)
        if prop is None:
            return default
        return prop == "1"
