import logging

from pygame import Rect, Vector2
import pygame

from justkeepswimming.components.font import TextComponent
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.font import TextProcessor
from justkeepswimming.processors.render import RendererPreProcessor, RendererProcessor
from justkeepswimming.processors.sizing import RendererTransformConstraintProcessor
from justkeepswimming.processors.tile import TileTextureProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext

logger = logging.getLogger(__name__)


def is_point_in_bounds(
    point: Vector2, top_left: Vector2, bottom_right: Vector2
) -> bool:
    return (
        top_left.x <= point.x <= bottom_right.x
        and top_left.y <= point.y <= bottom_right.y
    )


class ButtonProcessor(Processor):
    reads = frozenset(
        {
            TransformComponent,
            ButtonComponent,
            RendererComponent,
            TextComponent,
        }
    )
    writes = frozenset(
        {
            ButtonComponent,
            RendererComponent,
            TextComponent,
        }
    )
    after = frozenset(
        {
            RendererTransformConstraintProcessor,
            RendererPreProcessor,
        }
    )
    before = frozenset({RendererProcessor, TextProcessor})
    alongside = frozenset({TileTextureProcessor})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for entity, (button, transform, renderer) in scene_context.query(
            ButtonComponent, TransformComponent, RendererComponent
        ):
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            rect.center = (int(transform.position.x), int(transform.position.y))
            colliding = rect.collidepoint(engine_context.input.mouse.position)
            if colliding and not button.hovering:
                await button.on_hover.emit()
            elif not colliding and button.hovering:
                await button.on_unhover.emit()
            button.hovering = colliding
            if button.hovering:
                pygame.draw.rect(
                    renderer.surface,
                    button.hover_background_color,
                    Rect(Vector2(0, 0), Vector2(rect.width, rect.height)),
                    border_radius=min(rect.width, rect.height) // 2,
                )
            else:
                pygame.draw.rect(
                    renderer.surface,
                    button.background_color,
                    Rect(Vector2(0, 0), Vector2(rect.width, rect.height)),
                    border_radius=min(rect.width, rect.height) // 2,
                )
            if entity.has_component(TextComponent):
                if button.hovering:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color_hover
                else:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color
