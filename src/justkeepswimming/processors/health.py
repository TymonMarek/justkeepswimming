from justkeepswimming.components.health import HealthComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext


class HealthProcessor(Processor):
    reads = frozenset({HealthComponent})
    writes = frozenset({HealthComponent})
    after = frozenset({})
    before = frozenset({})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for _, (health,) in scene_context.query(HealthComponent):
            if (
                health.current_health <= 0
                and not health.is_invincible
                and health.is_alive
            ):
                health.is_alive = False
                await health.on_died.emit()
