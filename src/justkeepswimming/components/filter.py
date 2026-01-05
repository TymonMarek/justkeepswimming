from dataclasses import dataclass, field

import pygame
from pygame import Color

from justkeepswimming.ecs import Component


@dataclass
class TintComponent(Component):
    intensity: float = 0.5
    color: Color = field(default_factory=lambda: Color(255, 255, 255))
    blend_mode: int = pygame.BLEND_RGBA_MULT
