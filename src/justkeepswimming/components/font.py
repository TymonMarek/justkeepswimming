from justkeepswimming.ecs import Component
from dataclasses import dataclass
from pygame.font import Font
from pygame import Color


@dataclass
class TextComponent(Component):
    color: Color
    font: Font
    text: str
