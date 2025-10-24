from snakia.core.tui import Canvas, Renderer


class PlainTextRenderer(Renderer):
    def render(self, canvas: Canvas) -> None:
        for y in range(canvas.height):
            for x in range(canvas.width):
                char = canvas.get(x, y)
                self.target.write(char.char)
            self.target.write("\n")

    def clear_screen(self) -> None:
        pass

    def hide_cursor(self) -> None:
        pass

    def show_cursor(self) -> None:
        pass

    def set_cursor_position(self, x: int, y: int) -> None:
        pass
