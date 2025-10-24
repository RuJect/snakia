from typing import Iterable

from snakia.core.tui import Widget
from snakia.core.tui.canvas import Canvas
from snakia.core.tui.char import CanvasChar

from .container import ContainerWidget


class VerticalSplitWidget(ContainerWidget):
    def __init__(
        self, children: Iterable[Widget], splitter_char: str = "-"
    ) -> None:
        super().__init__(children)
        self.splitter_char = splitter_char

    def on_render(self) -> Canvas:
        children_list = self.children.value
        if not children_list:
            return Canvas(0, 0, CanvasChar())

        child_canvases = [child.render() for child in children_list]
        max_width = max(canvas.width for canvas in child_canvases)
        total_height = (
            sum(canvas.height for canvas in child_canvases)
            + len(child_canvases)
            - 1
        )

        result = Canvas(max_width, total_height, CanvasChar())

        y_offset = 0
        for i, canvas in enumerate(child_canvases):
            result.copy_from(canvas, 0, y_offset)
            y_offset += canvas.height

            if i < len(child_canvases) - 1:
                splitter_char = CanvasChar(self.splitter_char)
                for x in range(max_width):
                    result.set(x, y_offset, splitter_char)
                y_offset += 1

        return result
