from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Color(BaseModel):
    model_config = ConfigDict(frozen=True)

    r: int = Field(default=0)
    g: int = Field(default=0)
    b: int = Field(default=0)
    a: int = Field(default=0xFF)

    @field_validator("r", mode="before")
    def _r_validator(self, value: int) -> int:
        return value & 0xFF

    @field_validator("g", mode="before")
    def _g_validator(self, value: int) -> int:
        return value & 0xFF

    @field_validator("b", mode="before")
    def _b_validator(self, value: int) -> int:
        return value & 0xFF

    @property
    def hex(self) -> str:
        """Return the color in hex format."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Return the color in rgb format."""
        return self.r, self.g, self.b

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """Return the color in rgba format."""
        return self.r, self.g, self.b, self.a

    @classmethod
    def from_hex(cls, hex_: str, /) -> Color:
        """
        Create a color from a hex string.

        Args:
            hex_: The hex string to create the color from.

        Returns:
            The color created from the hex string.
        """
        hex_ = hex_.lstrip("#")
        return cls(
            r=int(hex_[1:3], 16),
            g=int(hex_[3:5], 16),
            b=int(hex_[5:7], 16),
            a=int(hex_[7:9], 16) if len(hex_) >= 9 else 255,
        )

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: int = 255) -> Color:
        """
        Create a color from rgb values.

        Args:
            r (int): The red value.
            g (int): The green value.
            b (int): The blue value.
            a (int): The alpha value.

        Returns:
            Color: The color created from the rgb values.
        """
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
