import pygame
from pygame import Vector2

from justkeepswimming.components.animation import (
    AnimationStateComponent,
    AnimatorComponent,
    SpritesheetComponent,
    VelocityAffectsAnimationSpeedComponent,
)
from justkeepswimming.components.physics import (
    LinearPhysicsComponent,
    TransformComponent,
)
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.ecs import Processor, SceneContext
from justkeepswimming.processors.render import RendererPreProcessor, RendererProcessor
from justkeepswimming.processors.sizing import RendererTransformConstraintProcessor
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.animation import AnimationType
from justkeepswimming.utilities.context import EngineContext


class AnimationTrackPlaybackProcessor(Processor):
    reads = frozenset({AnimatorComponent, RendererComponent})
    writes = frozenset({AnimatorComponent, RendererComponent})
    before = frozenset({RendererProcessor})
    after = frozenset({RendererTransformConstraintProcessor, RendererPreProcessor})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (
            animator,
            renderer,
        ) in scene.query(
            AnimatorComponent,
            RendererComponent,
        ):
            await animator.animator.update(tick, scene)
            current_frame = await animator.animator.get_current_frame()
            if current_frame is not None:
                renderer.surface.blit(
                    pygame.transform.scale(current_frame, renderer.surface.get_size()),
                    Vector2(0, 0),
                )


class CharacterAnimationStateProcessor(Processor):
    reads = frozenset(
        {AnimationStateComponent, TransformComponent, LinearPhysicsComponent}
    )
    writes = frozenset({AnimationStateComponent})

    ACCEL_EPS = 0.1
    DOT_HYST = 0.2

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (animation_state, transform, physics) in scene.query(
            AnimationStateComponent,
            TransformComponent,
            LinearPhysicsComponent,
        ):
            acceleration = physics.acceleration.length()

            if acceleration <= self.ACCEL_EPS:
                if animation_state.current_state != AnimationType.IDLE:
                    animation_state.current_state = AnimationType.IDLE
                continue

            velocity = physics.velocity
            if velocity.length_squared() < 1e-6:
                desired = AnimationType.WALK
            else:
                move_direction = velocity.normalize()
                facing_direction = Vector2(1, 0).rotate(transform.rotation)
                dot = move_direction.dot(facing_direction)

                if animation_state.current_state == AnimationType.REVERSE_WALK:
                    desired = (
                        AnimationType.REVERSE_WALK
                        if dot < +self.DOT_HYST
                        else AnimationType.WALK
                    )
                else:
                    desired = (
                        AnimationType.WALK
                        if dot > -self.DOT_HYST
                        else AnimationType.REVERSE_WALK
                    )

            if animation_state.current_state != desired:
                animation_state.current_state = desired


class CharacterAnimationProcessor(Processor):
    reads = frozenset(
        {AnimatorComponent, AnimationStateComponent, SpritesheetComponent}
    )
    writes = frozenset({AnimatorComponent})
    before = frozenset({RendererProcessor, AnimationTrackPlaybackProcessor})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (
            animator,
            animation_state,
            spritesheet,
        ) in scene.query(
            AnimatorComponent,
            AnimationStateComponent,
            SpritesheetComponent,
        ):
            desired_animation = spritesheet.animations[animation_state.current_state]
            if (
                animation_state.current_track is None
                or animation_state.current_track.animation != desired_animation
            ):
                if (
                    animation_state.current_track is not None
                    and animation_state.current_track.priority.value
                    >= desired_animation.priority.value
                ):
                    await animation_state.current_track.stop()
                animation_state.current_track = await animator.animator.load_animation(
                    animation_state.current_state, desired_animation
                )
                await animation_state.current_track.play()


class VelocityAffectsAnimationSpeedProcessor(Processor):
    reads = frozenset(
        {
            AnimationStateComponent,
            LinearPhysicsComponent,
            VelocityAffectsAnimationSpeedComponent,
        }
    )
    writes = frozenset({AnimationStateComponent})
    before = frozenset({})
    after = frozenset({CharacterAnimationStateProcessor})

    async def update(
        self,
        tick: TickContext,
        scene: SceneContext,
        engine: EngineContext,
    ) -> None:
        for _, (
            animation_state,
            linear_physics,
            velocity_affects_animation_speed,
        ) in scene.query(
            AnimationStateComponent,
            LinearPhysicsComponent,
            VelocityAffectsAnimationSpeedComponent,
        ):
            if track := animation_state.current_track:
                base_speed = track.animation.speed
                speed = (
                    linear_physics.velocity.length()
                    * velocity_affects_animation_speed.speed_multiplier
                )
                animation_state.current_speed = base_speed + speed
