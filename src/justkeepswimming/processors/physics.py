from pygame import Vector2

from justkeepswimming.components.input import (
    PlayerAngularMovementInputComponent,
    PlayerLinearMovementInputComponent,
)
from justkeepswimming.components.physics import (
    AngularPhysicsComponent,
    LinearPhysicsComponent,
    TransformComponent,
)
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext


class AngularPhysicsProcessor(Processor):
    reads = frozenset({AngularPhysicsComponent, PlayerAngularMovementInputComponent})
    writes = frozenset({TransformComponent, AngularPhysicsComponent})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        delta = tick_context.delta_time * scene_context.time_scale

        for entity, (angular_physics, transform) in scene_context.query(
            AngularPhysicsComponent,
            TransformComponent,
        ):
            torque_acceleration: float = 0.0

            if entity.has_component(PlayerAngularMovementInputComponent):
                input_component = entity.get_component(
                    PlayerAngularMovementInputComponent
                )

                torque_acceleration = input_component.torque * angular_physics.torque

            angular_physics.angular_velocity += torque_acceleration * delta
            angular_physics.angular_velocity -= (
                angular_physics.angular_velocity * angular_physics.angular_drag * delta
            )

            if (
                abs(angular_physics.angular_velocity)
                > angular_physics.max_angular_velocity
            ):
                angular_physics.angular_velocity = (
                    angular_physics.max_angular_velocity
                    * (1 if angular_physics.angular_velocity > 0 else -1)
                )

            transform.rotation += angular_physics.angular_velocity * delta


class LinearPhysicsProcessor(Processor):
    reads = frozenset({LinearPhysicsComponent, PlayerLinearMovementInputComponent})
    writes = frozenset({TransformComponent, LinearPhysicsComponent})
    alongside = frozenset({AngularPhysicsProcessor})

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        delta = tick_context.delta_time * scene_context.time_scale

        for entity, (linear_physics, transform) in scene_context.query(
            LinearPhysicsComponent,
            TransformComponent,
        ):
            wish_direction = Vector2()

            if entity.has_component(PlayerLinearMovementInputComponent):
                input_component = entity.get_component(
                    PlayerLinearMovementInputComponent
                )

                wish_direction = input_component.thrust

                if wish_direction.length_squared() > 1:
                    wish_direction = wish_direction.normalize()

            if wish_direction.x or wish_direction.y:
                thrust = linear_physics.thrust
                linear_physics.acceleration = (
                    wish_direction.elementwise() * thrust
                ).rotate(transform.rotation)
            else:
                linear_physics.acceleration.update(0.0, 0.0)

            linear_physics.velocity += linear_physics.acceleration * delta

            drag = linear_physics.drag
            decay_x = 1 - drag.x * delta
            decay_y = 1 - drag.y * delta
            if decay_x < 0:
                decay_x = 0
            if decay_y < 0:
                decay_y = 0

            linear_physics.velocity.x *= decay_x
            linear_physics.velocity.y *= decay_y

            max_v = linear_physics.max_velocity
            linear_physics.velocity.x = max(
                -max_v.x, min(linear_physics.velocity.x, max_v.x)
            )
            linear_physics.velocity.y = max(
                -max_v.y, min(linear_physics.velocity.y, max_v.y)
            )

            transform.position += linear_physics.velocity * delta
