from justkeepswimming.components.animation import (
    AnimationStateComponent,
    AnimatorComponent,
    SpritesheetComponent,
    VelocityAffectsAnimationSpeedComponent,
)
from justkeepswimming.prefabs.renderable import RenderablePrefab
from justkeepswimming.processors.animation import (
    AnimationTrackPlaybackProcessor,
    CharacterAnimationProcessor,
    CharacterAnimationStateProcessor,
    VelocityAffectsAnimationSpeedProcessor,
)
from justkeepswimming.utilities.prefab import Prefab


class CharacterPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        AnimatorComponent(),
        AnimationStateComponent(),
        SpritesheetComponent({}),
        VelocityAffectsAnimationSpeedComponent(),
    ]
    processors = [
        AnimationTrackPlaybackProcessor,
        CharacterAnimationStateProcessor,
        CharacterAnimationProcessor,
        VelocityAffectsAnimationSpeedProcessor,
    ]
