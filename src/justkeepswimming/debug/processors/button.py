import logging

from pygame import Color, Rect, Vector2
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.pseudo import ScenePseudoComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.debug.processors.rendering import MouseDebuggerProcessor, RendererDebuggerProcessor
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.position import SceneCenterConstraintProcessor
from justkeepswimming.processors.render import RendererProcessor
from justkeepswimming.processors.sizing import SceneSizeConstraintProcessor
from justkeepswimming.processors.tile import AutoTileScrollProcessor, MouseRelativeTileScrollProcessor
from justkeepswimming.processors.ui import ButtonProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.rendering import DEBUG_FONT, render_bounding_box, render_connection, render_label

logger = logging.getLogger(__name__)


def is_point_in_bounds(
    point: Vector2, top_left: Vector2, bottom_right: Vector2
) -> bool:
    return (
        top_left.x <= point.x <= bottom_right.x
        and top_left.y <= point.y <= bottom_right.y
    )


class ButtonDebuggerProcessor(Processor):
    reads = frozenset({TransformComponent, ButtonComponent, RendererComponent})
    writes = frozenset({ScenePseudoComponent})
    after = frozenset(
        {
            RendererProcessor,
            ButtonProcessor,
            SceneSizeConstraintProcessor,
            RendererProcessor,
            AutoTileScrollProcessor,
            SceneCenterConstraintProcessor,
            MouseRelativeTileScrollProcessor,
            RendererDebuggerProcessor,
            MouseDebuggerProcessor
        }
    )
    before = frozenset({})
    alongside = frozenset({})
    debug_only = True

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (button, transform, _) in scene_context.query(
            ButtonComponent, TransformComponent, RendererComponent
        ):
            rect = Rect()
            rect.width, rect.height = int(transform.size.x), int(transform.size.y)
            rect.center = (int(transform.position.x), int(transform.position.y))
            hovered = button.hovering
            render_label(
                scene_context.surface,
                Vector2(rect.left, rect.top - 15),
                f"{hovered}",
                DEBUG_FONT,
                Color(255, 0, 0) if hovered else Color(0, 255, 0),
            )
            render_bounding_box(
                scene_context.surface,
                rect,
                Color(0, 0, 255) if hovered else Color(0, 255, 0),
                2,
            )
            render_connection(
                scene_context.surface,
                Vector2(rect.center),
                engine_context.input.mouse.position,
                Color(0, 0, 255) if hovered else Color(0, 255, 0),
                2,
            )
