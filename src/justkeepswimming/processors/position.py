from pygame import Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.position import SceneCenterConstraintComponent
from justkeepswimming.components.pseudo import ScenePseudoComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.physics import (
    AngularPhysicsProcessor,
    LinearPhysicsProcessor,
)
from justkeepswimming.processors.render import RendererProcessor
from justkeepswimming.processors.sizing import SceneSizeConstraintProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext


class SceneCenterConstraintProcessor(Processor):
    reads = frozenset(
        {
            TransformComponent,
            SceneCenterConstraintComponent,
            ScenePseudoComponent,
        }
    )
    writes = frozenset({TransformComponent})
    after = frozenset({SceneSizeConstraintProcessor})
    before = frozenset({RendererProcessor})
    alongside = frozenset({LinearPhysicsProcessor, AngularPhysicsProcessor})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (transform, _) in scene.query(
            TransformComponent, SceneCenterConstraintComponent
        ):
            size = Vector2(scene.surface.get_size())
            transform.position.x = size.x / 2
            transform.position.y = size.y / 2
