import pygame
from pygame import Color

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.pseudo import ScenePseudoComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext

BACKGROUND_COLOR: Color = Color(0, 0, 0)


class RendererProcessor(Processor):
    reads = frozenset({TransformComponent, RendererComponent})
    writes = frozenset({RendererComponent, ScenePseudoComponent})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        scene.surface.fill(BACKGROUND_COLOR)
        entities = list(scene.query(TransformComponent, RendererComponent))
        entities.sort(key=lambda item: getattr(item[1][1], "layer", 0))
        for _, (transform, renderer) in entities:
            rotated_surface = pygame.transform.rotate(
                renderer.surface, -transform.rotation
            )
            rotated_rect = rotated_surface.get_rect()
            anchor_offset = transform.size.elementwise() * transform.anchor
            position = transform.position - anchor_offset
            rotated_rect.center = (int(position[0]), int(position[1]))
            scene.surface.blit(rotated_surface, rotated_rect.topleft)


class RendererPreProcessor(Processor):
    reads = frozenset({})
    writes = frozenset({RendererComponent})
    before = frozenset({RendererProcessor})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (renderer,) in scene.query(RendererComponent):
            renderer.surface.fill(Color(0, 0, 0, 0))
