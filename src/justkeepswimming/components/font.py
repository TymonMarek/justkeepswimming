from dataclasses import dataclass, field
from justkeepswimming.ecs import Component
from pygame.font import Font, SysFont
from pygame import Color


@dataclass
class TextComponent(Component):
    font: Font = field(default_factory=lambda: SysFont(None, 24))
    color: Color = field(default_factory=lambda: Color(0, 0, 0))
    background_color: Color = field(default_factory=lambda: Color(0, 0, 0, 0))
    antialias: bool = False
    autosize: bool = True
    content: str = ""

    def __deepcopy__(self, memo: dict[str, object]) -> "TextComponent":
        return TextComponent(
            font=self.font,
            color=self.color,
            background_color=self.background_color,
            antialias=self.antialias,
            content=self.content
        )

    def __hash__(self) -> int:
        return hash((
            self.font,
            str(self.color),
            str(self.background_color),
            self.antialias,
            self.content
        ))
