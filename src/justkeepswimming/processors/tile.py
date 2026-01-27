import logging
import math

import pygame

from pygame import Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.pseudo import ScenePseudoComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.tile import (
    AutoTileScrollComponent,
    FitTileSizeToTransformComponent,
    MouseRelativeTileScrollComponent,
    TileTextureComponent,
)
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.animation import AnimationTrackPlaybackProcessor
from justkeepswimming.processors.filter import TintProcessor
from justkeepswimming.processors.physics import (
    AngularPhysicsProcessor,
    LinearPhysicsProcessor,
)
from justkeepswimming.processors.render import RendererPreProcessor, RendererProcessor
from justkeepswimming.processors.sizing import RendererTransformConstraintProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext

pygame.font.init()
DEBUG_FONT = pygame.font.SysFont(None, 34)


class TileTextureProcessor(Processor):
    reads = frozenset({TileTextureComponent, TransformComponent})
    writes = frozenset({TileTextureComponent, RendererComponent})
    after = frozenset({RendererTransformConstraintProcessor, RendererPreProcessor})
    before = frozenset({RendererProcessor, TintProcessor})
    alongside = frozenset({AnimationTrackPlaybackProcessor})
    logger = logging.getLogger(__name__)

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (renderer, transform, tile_texture) in scene_context.query(
            RendererComponent, TransformComponent, TileTextureComponent
        ):
            surface = await tile_texture.image.get_surface()

            tile_w_f = float(tile_texture.tile_size.x)
            tile_h_f = float(tile_texture.tile_size.y)
            if tile_w_f <= 0.0 or tile_h_f <= 0.0:
                continue

            tile_w = int(tile_w_f)
            tile_h = int(tile_h_f)
            if tile_w <= 0 or tile_h <= 0:
                continue

            scroll = tile_texture.scroll
            scroll.x %= tile_w
            scroll.y %= tile_h

            src_id = id(surface)
            wh = (tile_w, tile_h)

            if (
                tile_texture.cache_scaled_surface is None
                or tile_texture.cache_src_id != src_id
                or tile_texture.cache_tile_wh != wh
            ):
                scaled_surface = pygame.transform.scale(surface, wh)
                tile_texture.cache_scaled_surface = scaled_surface
                tile_texture.cache_src_id = src_id
                tile_texture.cache_tile_wh = wh

            size_x = float(transform.size.x)
            size_y = float(transform.size.y)

            tiles_x = int(math.ceil(size_x / tile_w)) + 1
            tiles_y = int(math.ceil(size_y / tile_h)) + 1

            if (scroll.x * scroll.x + scroll.y * scroll.y) != 0.0:
                tiles_x += 2
                tiles_y += 2
                start_x = -1
                start_y = -1
            else:
                start_x = 0
                start_y = 0

            pos_x = transform.position.x
            pos_y = transform.position.y
            half_w = size_x * 0.5
            half_h = size_y * 0.5

            origin_x = pos_x - half_w - scroll.x
            origin_y = pos_y - half_h - scroll.y

            surf = renderer.surface

            end_x = start_x + tiles_x
            end_y = start_y + tiles_y

            for x in range(start_x, end_x):
                px = origin_x + x * tile_w
                for y in range(start_y, end_y):
                    py = origin_y + y * tile_h
                    surf.blit(tile_texture.cache_scaled_surface, Vector2(px, py))


class AutoTileScrollProcessor(Processor):
    reads = frozenset(
        {AutoTileScrollComponent, TileTextureComponent, ScenePseudoComponent}
    )
    writes = frozenset({TileTextureComponent})
    before = frozenset({TileTextureProcessor, RendererProcessor})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        delta = float(tick_context.delta_time * scene_context.time_scale)

        for _, (auto_tile_scroll, tile_texture) in scene_context.query(
            AutoTileScrollComponent, TileTextureComponent
        ):
            tile_size_x = float(tile_texture.tile_size.x) or 1.0
            tile_size_y = float(tile_texture.tile_size.y) or 1.0

            tile_texture.scroll += auto_tile_scroll.speed * delta
            tile_texture.scroll.x %= tile_size_x
            tile_texture.scroll.y %= tile_size_y


class FitTileSizeToTransformProcessor(Processor):
    reads = frozenset({FitTileSizeToTransformComponent, TransformComponent})
    writes = frozenset({TileTextureComponent})
    before = frozenset({TileTextureProcessor, AutoTileScrollProcessor})
    alongside = frozenset(
        {
            LinearPhysicsProcessor,
            AngularPhysicsProcessor,
            AnimationTrackPlaybackProcessor,
        }
    )

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (_, transform, tile_texture) in scene_context.query(
            FitTileSizeToTransformComponent,
            TransformComponent,
            TileTextureComponent,
        ):
            if transform.size.x and transform.size.y:
                tile_texture.tile_size = transform.size

def lerp_vec2(start: Vector2, end: Vector2, time: float) -> Vector2:
    return start + (end - start) * time

class MouseRelativeTileScrollProcessor(Processor):
    reads = frozenset(
        {MouseRelativeTileScrollComponent, TileTextureComponent, ScenePseudoComponent}
    )
    writes = frozenset({TileTextureComponent})
    after = frozenset({FitTileSizeToTransformProcessor, AutoTileScrollProcessor})
    before = frozenset({TileTextureProcessor, RendererProcessor})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (mouse_relative_scroll, tile_texture) in scene_context.query(
            MouseRelativeTileScrollComponent, TileTextureComponent
        ):
            screen_center = engine_context.window.size * 0.5
            mouse_position = engine_context.input.mouse.position
            mouse_relative = (mouse_position - screen_center).elementwise() / screen_center
            tile_texture.scroll = mouse_relative.elementwise() * mouse_relative_scroll.strength
