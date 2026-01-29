from justkeepswimming.components.filter import TintComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.animation import AnimationTrackPlaybackProcessor
from justkeepswimming.processors.render import RendererPreProcessor, RendererProcessor
from justkeepswimming.processors.sizing import RendererTransformConstraintProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext


class TintProcessor(Processor):
    reads = frozenset({TintComponent, RendererComponent})
    writes = frozenset({RendererComponent})
    after = frozenset(
        {
            RendererPreProcessor,
            AnimationTrackPlaybackProcessor,
            RendererTransformConstraintProcessor,
        }
    )
    before = frozenset({RendererProcessor})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (tint_component, renderable_component) in scene_context.query(
            TintComponent, RendererComponent
        ):
            tint_color = tint_component.color
            intensity = tint_component.intensity
            blended_color = (
                int(tint_color.r * intensity),
                int(tint_color.g * intensity),
                int(tint_color.b * intensity),
                int(tint_color.a * intensity),
            )
            tint_surface = renderable_component.surface.copy()
            tint_surface.fill(
                blended_color, special_flags=tint_component.blend_mode)
            renderable_component.surface.blit(tint_surface, (0, 0))
