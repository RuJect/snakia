from __future__ import annotations

from typing import Final, Iterable

from .char import CanvasChar


class Canvas:
    """
    A canvas is a 2D array of characters.
    """

    __slots__ = "__buffer", "__default", "width", "height"

    def __init__(
        self, width: int, height: int, default_value: CanvasChar = CanvasChar()
    ) -> None:
        width = max(width, 0)
        height = max(height, 0)

        self.width: Final[int] = width
        self.height: Final[int] = height
        self.__default: Final[CanvasChar] = default_value

        self.__buffer: list[CanvasChar] = [default_value] * self.total

    @property
    def total(self) -> int:
        return self.width * self.height

    def get(self, x: int, y: int, /) -> CanvasChar:
        """Get the character at the given position."""
        return self.__buffer[self._get_index(x, y)]

    def get_row(self, y: int, /) -> Iterable[CanvasChar]:
        """Get the row at the given position."""
        start_index = self._get_index(0, y)
        end_index = start_index + self.width
        return self.__buffer[start_index:end_index]

    def get_column(self, x: int, /) -> Iterable[CanvasChar]:
        """Get the column at the given position."""
        return (
            self.__buffer[self._get_index(x, y)] for y in range(self.height)
        )

    def set(self, x: int, y: int, value: CanvasChar, /) -> None:
        """Set the character at the given position."""
        self.__buffer[self._get_index(x, y)] = value

    def set_row(self, y: int, value: CanvasChar, /) -> None:
        """Set the row at the given position."""
        start_index = self._get_index(0, y)
        end_index = start_index + self.width
        self.__buffer[start_index:end_index] = [value] * self.width

    def set_column(self, x: int, value: CanvasChar, /) -> None:
        """Set the column at the given position."""
        for y in range(self.height):
            self.set(x, y, value)

    def set_area(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        value: CanvasChar,
    ) -> None:
        """Set the area at the given position."""
        for dy in range(height):  # TODO: optimize
            for dx in range(width):
                self.set(x + dx, y + dy, value)

    def clear(self) -> None:
        """Clear the canvas."""
        self.fill(self.__default)

    def fill(self, value: CanvasChar, /) -> None:
        """Fill the canvas with the given value."""
        self.__buffer = [value] * self.total

    def draw_line_h(
        self,
        x: int,
        y: int,
        length: int,
        char: CanvasChar,
    ) -> None:
        """Draw a horizontal line."""
        for i in range(length):
            self.set(x + i, y, char)

    def draw_line_v(
        self,
        x: int,
        y: int,
        length: int,
        char: CanvasChar,
    ) -> None:
        """Draw a vertical line."""
        for i in range(length):
            self.set(x, y + i, char)

    def draw_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        char: CanvasChar,
    ) -> None:
        """Draw a rectangle."""
        # Bottom and top
        self.draw_line_h(x, y, width, char)
        self.draw_line_h(x, y + height - 1, width, char)

        # Left and right
        self.draw_line_v(x, y, height, char)
        self.draw_line_v(x + width - 1, y, height, char)

    def copy_from(self, other: Canvas, x: int = 0, y: int = 0) -> None:
        """Copy the given canvas to the current canvas."""
        for dy in range(min(other.height, self.height - y)):
            for dx in range(min(other.width, self.width - x)):
                self.set(x + dx, y + dy, other.get(dx, dy))

    def draw_text(self, x: int, y: int, text: str, char: CanvasChar) -> None:
        """Draw text on the canvas."""
        for i, c in enumerate(text):
            if x + i < self.width:
                self.set(
                    x + i,
                    y,
                    CanvasChar(
                        char=c,
                        fg_color=char.fg_color,
                        bg_color=char.bg_color,
                        bold=char.bold,
                        italic=char.italic,
                        underline=char.underline,
                    ),
                )

    def draw_filled_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        char: CanvasChar,
    ) -> None:
        """Draw a filled rectangle."""
        for dy in range(height):
            for dx in range(width):
                self.set(x + dx, y + dy, char)

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given position is valid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_subcanvas(self, x: int, y: int, width: int, height: int) -> Canvas:
        """Get a subcanvas from the current canvas."""
        subcanvas = Canvas(width, height, self.__default)
        for dy in range(height):
            for dx in range(width):
                if self.is_valid_position(x + dx, y + dy):
                    subcanvas.set(dx, dy, self.get(x + dx, y + dy))
        return subcanvas

    def _get_index(self, x: int, y: int) -> int:
        return self.width * y + x
