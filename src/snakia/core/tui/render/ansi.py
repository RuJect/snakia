from snakia.core.tui import Canvas, CanvasChar, Renderer, RenderTarget


class ANSIRenderer(Renderer):
    def __init__(self, target: RenderTarget) -> None:
        super().__init__(target)
        self._current_char = CanvasChar()

    def render(self, canvas: Canvas) -> None:
        for y in range(canvas.height):
            for x in range(canvas.width):
                char = canvas.get(x, y)
                self._render_char(char)
            self.target.write("\n")

    def _render_char(self, char: CanvasChar) -> None:
        if char != self._current_char:
            self._reset_attributes()
            self._apply_attributes(char)
            self._current_char = char
        self.target.write(char.char)

    def _reset_attributes(self) -> None:
        self.target.write("\033[0m")

    def _apply_attributes(self, char: CanvasChar) -> None:
        codes = []

        if char.bold:
            codes.append("1")
        if char.italic:
            codes.append("3")
        if char.underline:
            codes.append("4")

        if char.fg_color:
            codes.append(f"38;5;{self._color_to_ansi(char.fg_color)}")
        if char.bg_color:
            codes.append(f"48;5;{self._color_to_ansi(char.bg_color)}")

        if codes:
            self.target.write(f"\033[{';'.join(codes)}m")

    def _color_to_ansi(self, color: str) -> int:
        color_map = {
            "black": 0,
            "red": 1,
            "green": 2,
            "yellow": 3,
            "blue": 4,
            "magenta": 5,
            "cyan": 6,
            "white": 7,
            "bright_black": 8,
            "bright_red": 9,
            "bright_green": 10,
            "bright_yellow": 11,
            "bright_blue": 12,
            "bright_magenta": 13,
            "bright_cyan": 14,
            "bright_white": 15,
        }
        return color_map.get(color.lower(), 7)

    def clear_screen(self) -> None:
        self.target.write("\033[2J")

    def hide_cursor(self) -> None:
        self.target.write("\033[?25l")

    def show_cursor(self) -> None:
        self.target.write("\033[?25h")

    def set_cursor_position(self, x: int, y: int) -> None:
        self.target.write(f"\033[{y + 1};{x + 1}H")
