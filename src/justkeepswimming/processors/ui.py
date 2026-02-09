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
from justkeepswimming.systems.input import MouseButton
from justkeepswimming.utilities.context import EngineContext


def is_point_in_bounds(point: Vector2, top_left: Vector2, bottom_right: Vector2) -> bool:
    return top_left.x <= point.x <= bottom_right.x and top_left.y <= point.y <= bottom_right.y


class ButtonProcessor(Processor):
    reads = frozenset({
        TransformComponent,
        ButtonComponent,
        RendererComponent,
        TextComponent,
    })
    writes = frozenset({
        ButtonComponent,
        RendererComponent,
        TextComponent,
    })
    after = frozenset({
        RendererTransformConstraintProcessor,
        RendererPreProcessor,
    })
    before = frozenset({
        RendererProcessor,
        TextProcessor
    })
    alongside = frozenset({
        TileTextureProcessor
    })

    async def on_mouse_moved(
        self,
        scene_context: SceneContext,
        new_position: Vector2
        ) -> None:
        for entity, (button, transform) in scene_context.query(ButtonComponent, TransformComponent):
            # TODO: consider doing top_left and bottom_right within the transform component itself
            # TODO: as a cached property
            bottom_right = transform.position + Vector2(
                transform.position.elementwise() + transform.size
            )
            top_left = transform.position
            hovered = is_point_in_bounds(new_position, top_left, bottom_right)
            if hovered:
                if not button.is_hovered:
                    button.is_hovered = True
                    await button.on_hover.emit()
                    if entity.has_component(TextComponent):
                        text = entity.get_component(TextComponent)
                        text.color = button.label_color_hover
            else:
                if button.is_hovered:
                    button.is_hovered = False
                    await button.on_unhover.emit()
                    if entity.has_component(TextComponent):
                        text = entity.get_component(TextComponent)
                        text.color = button.label_color

    async def on_mouse_button_pressed(
        self,
        scene_context: SceneContext,
        button: MouseButton
    ) -> None:
        for _, (button_component, transform) in scene_context.query(ButtonComponent, TransformComponent):
            bottom_right = transform.position + Vector2(
                transform.position.elementwise() + transform.size
            )
            top_left = transform.position
            if is_point_in_bounds(transform.position, top_left, bottom_right):
                await button_component.on_click.emit()

    async def on_mouse_button_released(
        self,
        scene_context: SceneContext,
        button: MouseButton
    ) -> None:
        for _, (button_component, transform) in scene_context.query(ButtonComponent, TransformComponent):
            bottom_right = transform.position + Vector2(
                transform.position.elementwise() + transform.size
            )
            top_left = transform.position
            if is_point_in_bounds(transform.position, top_left, bottom_right):
                await button_component.on_release.emit()

    def initialize(
        self,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        engine_context.input.mouse.on_mouse_move.connect(lambda position: self.on_mouse_moved(scene_context, position))
        engine_context.input.mouse.on_mouse_button_pressed.connect(lambda button: self.on_mouse_button_pressed(scene_context, button))
        engine_context.input.mouse.on_mouse_button_released.connect(lambda button: self.on_mouse_button_released(scene_context, button))

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for entity, (button, transform, renderer) in scene_context.query(ButtonComponent, TransformComponent, RendererComponent):
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            if button.is_hovered:
                pygame.draw.rect(
                    renderer.surface,
                    button.hover_background_color,
                    rect,
                    border_radius=min(rect.width, rect.height) // 2 
                )
            else:
                pygame.draw.rect(
                    renderer.surface,
                    button.background_color,
                    rect,
                    border_radius=min(rect.width, rect.height) // 2 
                )
            if entity.has_component(TextComponent):
                if button.is_hovered:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color_hover
                else:
                    text = entity.get_component(TextComponent)
                    text.color = button.label_color
            pygame.image.save(renderer.surface, "button_debug.png")
