from snakia.core.tui import Widget
from snakia.core.tui.canvas import Canvas
from snakia.core.tui.char import CanvasChar


class BoxWidget(Widget):
    def __init__(
        self, width: int, height: int, char: CanvasChar = CanvasChar("█")
    ) -> None:
        super().__init__()
        self.width = self.state(width)
        self.height = self.state(height)
        self.char = self.state(char)

    def on_render(self) -> Canvas:
        width = self.width.value
        height = self.height.value
        char = self.char.value
        canvas = Canvas(width, height, CanvasChar())
        canvas.draw_filled_rect(0, 0, width, height, char)
        return canvas
