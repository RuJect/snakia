from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field


class Color(BaseModel):
    model_config = ConfigDict(frozen=True)

    r: int = Field(default=0, ge=0x00, le=0xFF)
    g: int = Field(default=0, ge=0x00, le=0xFF)
    b: int = Field(default=0, ge=0x00, le=0xFF)
    a: int = Field(default=0xFF, ge=0x00, le=0xFF)

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a

    @classmethod
    def from_hex(cls, hex: str) -> Color:
        hex = hex.lstrip("#")
        return cls(
            r=int(hex[1:3], 16),
            g=int(hex[3:5], 16),
            b=int(hex[5:7], 16),
            a=int(hex[7:9], 16) if len(hex) >= 9 else 255,
        )

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: int = 255) -> Color:
        return cls(r=r, g=g, b=b, a=a)

    def __add__(self, other: Color) -> Color:
        return Color(
            r=self.r + other.r,
            g=self.g + other.g,
            b=self.b + other.b,
            a=self.a + other.a,
        )

    def __sub__(self, other: Color) -> Color:
        return Color(
            r=self.r - other.r,
            g=self.g - other.g,
            b=self.b - other.b,
            a=self.a - other.a,
        )


BLACK: Final[Color] = Color.from_hex("#000000")
WHITE: Final[Color] = Color.from_hex("#ffffff")
RED: Final[Color] = Color.from_hex("#ff0000")
GREEN: Final[Color] = Color.from_hex("#00ff00")
BLUE: Final[Color] = Color.from_hex("#0000ff")
YELLOW: Final[Color] = Color.from_hex("#ffff00")
CYAN: Final[Color] = Color.from_hex("#00ffff")
MAGENTA: Final[Color] = Color.from_hex("#ff00ff")
GRAY: Final[Color] = Color.from_hex("#808080")
DARK_GRAY: Final[Color] = Color.from_hex("#404040")
LIGHT_GRAY: Final[Color] = Color.from_hex("#c0c0c0")
DARK_RED: Final[Color] = Color.from_hex("#800000")
DARK_GREEN: Final[Color] = Color.from_hex("#008000")
DARK_BLUE: Final[Color] = Color.from_hex("#000080")
DARK_YELLOW: Final[Color] = Color.from_hex("#808000")
DARK_CYAN: Final[Color] = Color.from_hex("#008080")
DARK_MAGENTA: Final[Color] = Color.from_hex("#800080")
