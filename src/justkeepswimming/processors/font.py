from pygame import Color, Surface
from justkeepswimming.components.font import TextComponent
from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.ecs import Component, Processor, SceneContext
from justkeepswimming.processors.render import (
    RendererPreProcessor,
    RendererProcessor
)
from justkeepswimming.processors.sizing import (
    RendererTransformConstraintProcessor,
)
from justkeepswimming.processors.tile import TileTextureProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext


RENDER_CACHE: dict[int, Surface] = {}
RENDER_CACHE_LINKS: dict[TextComponent, int] = {}


class TextProcessor(Processor):
    writes: frozenset[type[Component]] = frozenset({
        RendererComponent,
    })
    reads: frozenset[type[Component]] = frozenset({
        TextComponent,
        TransformComponent
    })
    before: frozenset[type["Processor"]] = frozenset({
        RendererProcessor
    })
    after: frozenset[type["Processor"]] = frozenset({
        RendererTransformConstraintProcessor,
        RendererPreProcessor
    })
    alongside: frozenset[type["Processor"]] = frozenset({
        TileTextureProcessor
    })

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (text, renderer) in scene_context.query(
            TextComponent,
            RendererComponent,
        ):
            cached = RENDER_CACHE.get(hash(text))
            if cached is None:
                bg_color = (
                    text.background_color
                    if text.background_color.a > 0
                    else None
                )
                cached = text.font.render(
                    text.content or "",
                    text.antialias or True,
                    text.color or Color(0, 0, 0),
                    bg_color,
                ).convert_alpha()
                RENDER_CACHE[hash(text)] = cached
                if RENDER_CACHE_LINKS.get(text):
                    del RENDER_CACHE[RENDER_CACHE_LINKS[text]]
                RENDER_CACHE_LINKS[text] = hash(text)
            renderer.surface = cached
