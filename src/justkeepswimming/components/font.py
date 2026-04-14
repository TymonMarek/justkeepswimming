from dataclasses import dataclass, field
from enum import Enum
from justkeepswimming.ecs import Component
from pygame.font import Font, SysFont
from pygame import Color, Vector2


class TextAlignment(Enum):
    TOP_LEFT = Vector2(0, 0)
    LEFT = Vector2(0, 0.5)
    BOTTOM_LEFT = Vector2(0, 1)
    TOP = Vector2(0.5, 0)
    CENTER = Vector2(0.5, 0.5)
    BOTTOM = Vector2(0.5, 1)
    TOP_RIGHT = Vector2(1, 0)
    RIGHT = Vector2(1, 0.5)
    BOTTOM_RIGHT = Vector2(1, 1)


@dataclass
class TextComponent(Component):
    font: Font = field(default_factory=lambda: SysFont(None, 24))
    color: Color = field(default_factory=lambda: Color(0, 0, 0))
    background_color: Color = field(default_factory=lambda: Color(0, 0, 0, 0))
    alignment: TextAlignment = field(
        default_factory=lambda: TextAlignment.CENTER
    )
    antialias: bool = False
    autosize: bool = False
    content: str = ""

    def __deepcopy__(self, memo: dict[str, object]) -> "TextComponent":
        return TextComponent(
            font=self.font,
            color=self.color,
            background_color=self.background_color,
            antialias=self.antialias,
            content=self.content,
            autosize=self.autosize,
            alignment=self.alignment,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.font,
                str(self.color),
                str(self.background_color),
                self.antialias,
                self.content,
                self.autosize,
                self.alignment,
            )
        )
