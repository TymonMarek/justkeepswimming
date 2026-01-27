from dataclasses import dataclass, field

import pygame
from pygame import Vector2

from justkeepswimming.ecs import Component
from justkeepswimming.utilities.image import Image


@dataclass
class TileTextureComponent(Component):
    image: Image
    tile_size: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    scroll: Vector2 = field(default_factory=lambda: Vector2(0, 0))

    cache_src_id: int | None = field(default=None)
    cache_tile_wh: tuple[int, int] | None = field(default=None)
    cache_scaled_surface: pygame.Surface | None = field(default=None)


@dataclass
class AutoTileScrollComponent(Component):
    speed: Vector2


@dataclass
class MouseRelativeTileScrollComponent(Component):
    strength: Vector2
    lerp_factor: float = 0.1

@dataclass
class FitTileSizeToTransformComponent(Component):
    pass
