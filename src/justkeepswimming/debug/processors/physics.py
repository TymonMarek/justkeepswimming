from pygame import Color, Vector2

from justkeepswimming.components.input import PlayerLinearMovementInputComponent
from justkeepswimming.components.physics import (
    LinearPhysicsComponent,
    TransformComponent,
)
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.rendering import render_arrow, render_label


class LinearPhysicsDebuggerProcessor(Processor):
    reads = frozenset({LinearPhysicsComponent, PlayerLinearMovementInputComponent})
    writes = frozenset({})
    debug_only = True

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:

        surface = scene_context.surface
        font = engine_context.debug_font

        for entity, (linear_physics, transform) in scene_context.query(
            LinearPhysicsComponent,
            TransformComponent,
        ):
            origin = Vector2(transform.position)

            if entity.has_component(PlayerLinearMovementInputComponent):
                input = entity.get_component(PlayerLinearMovementInputComponent).thrust
                if input.length() > 0:
                    magnitude = input.normalize() * 25
                    render_arrow(
                        surface, origin, origin + magnitude, Color(255, 255, 0), 2
                    )
                    render_label(surface, origin + magnitude, "input", font)

            velocity = linear_physics.velocity
            if velocity.length() > 0:
                render_arrow(surface, origin, origin + velocity, Color(0, 255, 0), 2)
                render_label(surface, origin + velocity, "velocity", font)

            acceleration = linear_physics.acceleration
            if acceleration.length() > 0:
                render_arrow(
                    surface, origin, origin + acceleration, Color(255, 0, 0), 2
                )
                render_label(surface, origin + acceleration, "acceleration", font)
