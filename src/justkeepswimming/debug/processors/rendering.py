import pygame
from pygame import Color, Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.pseudo import ScenePseudoComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.position import SceneCenterConstraintProcessor
from justkeepswimming.processors.render import RendererProcessor
from justkeepswimming.processors.sizing import SceneSizeConstraintProcessor
from justkeepswimming.processors.tile import (
    AutoTileScrollProcessor,
    MouseRelativeTileScrollProcessor,
)
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.rendering import (
    render_bounding_box,
    render_cross,
)

BACKGROUND_COLOR: Color = Color(0, 0, 0)


class RendererDebuggerProcessor(Processor):
    reads = frozenset({TransformComponent, RendererComponent})
    writes = frozenset({ScenePseudoComponent})
    after = frozenset(
        {
            SceneSizeConstraintProcessor,
            RendererProcessor,
            AutoTileScrollProcessor,
            SceneCenterConstraintProcessor,
            MouseRelativeTileScrollProcessor,
        }
    )
    debug_only = True

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        scene = scene_context.surface
        entities = list(
            scene_context.query(TransformComponent, RendererComponent)
        )
        entities.sort(key=lambda item: getattr(item[1][1], "layer", 0))
        index = 0
        for _, (transform, renderer) in entities:
            index += 1
            rotated_surface = pygame.transform.rotate(
                renderer.surface, -transform.rotation
            )
            rotated_rect = rotated_surface.get_rect()
            rotated_rect.center = (
                int(transform.position[0]),
                int(transform.position[1]),
            )
            render_bounding_box(scene, rotated_rect, Color(255, 0, 0), 3)


class MouseDebuggerProcessor(Processor):
    reads = frozenset({TransformComponent, RendererComponent})
    writes = frozenset({ScenePseudoComponent})
    after = frozenset(
        {
            SceneSizeConstraintProcessor,
            RendererProcessor,
            AutoTileScrollProcessor,
            SceneCenterConstraintProcessor,
            MouseRelativeTileScrollProcessor,
            RendererDebuggerProcessor,
        }
    )
    debug_only = True

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        scene = scene_context.surface
        mouse_pos = engine_context.input.mouse.position
        render_cross(
            scene,
            Vector2(mouse_pos),
            size=1000,
            color=Color(255, 0, 0),
            thickness=2,
        )
