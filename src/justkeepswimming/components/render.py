from dataclasses import dataclass, field

import pygame
from pygame import Color, Surface, Vector2

from justkeepswimming.ecs import Component
from justkeepswimming.utilities.image import Image


@dataclass
class MainCameraComponent(Component):
    pass


@dataclass
class CameraComponent(Component):
    surface: Surface = field(default_factory=lambda: Surface((0, 0)))


@dataclass
class RendererComponent(Component):
    surface: Surface = field(
        default_factory=lambda: Surface(Vector2(0, 0), flags=pygame.SRCALPHA)
    )
    background: Color = field(default_factory=lambda: Color(0, 0, 0, 0))
    layer: int = 0


class SpriteComponent(Component):
    texture: Image
