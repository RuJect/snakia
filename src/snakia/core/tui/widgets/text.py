from snakia.core.tui import Widget
from snakia.core.tui.canvas import Canvas
from snakia.core.tui.char import CanvasChar


class TextWidget(Widget):
    def __init__(self, text: str, char: CanvasChar = CanvasChar()) -> None:
        super().__init__()
        self.text = self.state(text)
        self.char = self.state(char)

    def on_render(self) -> Canvas:
        text = self.text.value
        char = self.char.value
        canvas = Canvas(len(text), 1, CanvasChar())
        canvas.draw_text(0, 0, text, char)
        return canvas
