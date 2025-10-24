from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CanvasChar:
    char: str = " "
    fg_color: str | None = None
    bg_color: str | None = None
    bold: bool = False
    italic: bool = False
    underline: bool = False

    def __str__(self) -> str:
        return self.char

    def __repr__(self) -> str:
        attrs = []
        if self.fg_color:
            attrs.append(f"fg={self.fg_color}")
        if self.bg_color:
            attrs.append(f"bg={self.bg_color}")
        if self.bold:
            attrs.append("bold")
        if self.italic:
            attrs.append("italic")
        if self.underline:
            attrs.append("underline")

        attr_str = f"[{', '.join(attrs)}]" if attrs else ""
        return f"CanvasChar('{self.char}'{attr_str})"
