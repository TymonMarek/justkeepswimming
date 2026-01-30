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
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (tint, renderer) in scene.query(TintComponent, RendererComponent):
            tint_color = tint.color
            intensity = tint.intensity
            blended_color = (
                int(tint_color.r * intensity),
                int(tint_color.g * intensity),
                int(tint_color.b * intensity),
                int(tint_color.a * intensity),
            )
            tint_surface = renderer.surface.copy()
            tint_surface.fill(blended_color, special_flags=tint.blend_mode)
            renderer.surface.blit(tint_surface, (0, 0))
