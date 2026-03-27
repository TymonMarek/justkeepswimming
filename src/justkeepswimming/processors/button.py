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
from justkeepswimming.systems.input import Mouse, MouseButton
from justkeepswimming.utilities.context import EngineContext

logger = logging.getLogger(__name__)


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

    async def on_mouse_moved(
        self,
        scene_context: SceneContext,
        mouse: Mouse
        ) -> None:
        for entity, (button, transform) in scene_context.query(ButtonComponent, TransformComponent):
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            rect.center = (int(transform.position.x), int(transform.position.y))
            colliding = rect.collidepoint(mouse.position)
            if colliding:
                if not button.hovering:
                    button.hovering = True
                    logger.debug(f"Mouse is hovering over {entity.name}")
                    await button.on_hover.emit()
                    if entity.has_component(TextComponent):
                        text = entity.get_component(TextComponent)
                        text.color = button.label_color_hover
            else:
                if button.hovering:
                    button.hovering = False
                    logger.debug(f"Mouse is no longer hovering over {entity.name}")
                    await button.on_unhover.emit()
                    if entity.has_component(TextComponent):
                        text = entity.get_component(TextComponent)
                        text.color = button.label_color

    async def on_mouse_button_pressed(
        self,
        scene_context: SceneContext,
        mouse: Mouse,
        mouse_button: MouseButton
    ) -> None:
        for entity, (button, transform) in scene_context.query(ButtonComponent, TransformComponent):
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            rect.center = (int(transform.position.x), int(transform.position.y))
            colliding = rect.collidepoint(mouse.position)
            if colliding:
                logger.debug(f"Mouse button {mouse_button.button_type.name} pressed on {entity.name}")
                button.active = True
                await button.on_click.emit()

    async def on_mouse_button_released(
        self,
        scene_context: SceneContext,
        mouse: Mouse,
        mouse_button: MouseButton
    ) -> None:
        for entity, (button, transform) in scene_context.query(ButtonComponent, TransformComponent):
            if not button.active:
                continue
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            rect.center = (int(transform.position.x), int(transform.position.y))
            colliding = rect.collidepoint(mouse.position)
            button.active = False
            if colliding:
                logger.debug(
                    f"Mouse button {mouse_button.button_type.name} released on {entity.name}"
                )
                await button.on_release.emit()
            else:
                logger.debug(
                    f"Mouse button {mouse_button.button_type.name} cancelled press on {entity.name}"
                )

    def initialize(
        self,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        engine_context.input.mouse.on_mouse_move.connect(lambda mouse: self.on_mouse_moved(scene_context, mouse))
        engine_context.input.mouse.on_mouse_button_pressed.connect(lambda mouse, button: self.on_mouse_button_pressed(scene_context, mouse, button))
        engine_context.input.mouse.on_mouse_button_released.connect(lambda mouse, button: self.on_mouse_button_released(scene_context, mouse, button))

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
                    button.background_color_hover,
                    Rect(Vector2(0, 0), Vector2(rect.width, rect.height)),
                    border_radius=min(rect.width, rect.height) // 2,
                )
            elif button.active:
                pygame.draw.rect(
                    renderer.surface,
                    button.background_color_active,
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
                elif button.active:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color_active
                else:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color
