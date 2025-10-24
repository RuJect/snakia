import sys

from snakia.core.tui import CanvasChar, RenderContext
from snakia.core.tui.render import ANSIRenderer
from snakia.core.tui.widgets import (BoxWidget, HorizontalSplitWidget,
                                     TextWidget, VerticalSplitWidget)


class StdoutTarget:
    def write(self, text: str) -> None:
        sys.stdout.write(text)

    def flush(self) -> None:
        sys.stdout.flush()


def main() -> None:
    text1 = TextWidget("Hello", CanvasChar(fg_color="red", bold=True))
    text2 = TextWidget("World", CanvasChar(fg_color="blue", bold=True))
    text3 = TextWidget("Snakia", CanvasChar(fg_color="green", bold=True))

    box1 = BoxWidget(10, 3, CanvasChar("█", fg_color="yellow"))
    box2 = BoxWidget(8, 5, CanvasChar("█", fg_color="magenta"))

    horizontal_split = HorizontalSplitWidget([text1, text2, text3], "|")
    vertical_split = VerticalSplitWidget([horizontal_split, box1, box2], "-")

    renderer = ANSIRenderer(StdoutTarget())

    with RenderContext(renderer) as ctx:
        ctx.render(vertical_split.render())


if __name__ == "__main__":
    main()
