from pygame import Vector2

from justkeepswimming.characters.turtle import TurtlePrefab
from justkeepswimming.components.input import (
    PlayerAngularMovementInputComponent,
    PlayerLinearMovementInputComponent,
)
from justkeepswimming.components.physics import (
    AngularPhysicsComponent,
    LinearPhysicsComponent,
)
from justkeepswimming.components.player import PlayerComponent
from justkeepswimming.prefabs.physics import PhysicsObjectPrefab
from justkeepswimming.processors.input import (
    PlayerAngularMovementInputProcessor,
    PlayerLinearMovementInputProcessor,
)
from justkeepswimming.utilities.prefab import Prefab


class PlayerPrefab(Prefab):
    extends = [PhysicsObjectPrefab(), TurtlePrefab()]
    components = [
        LinearPhysicsComponent(
            thrust=Vector2(100.0, 50.0),
            max_velocity=Vector2(100.0, 50.0),
        ),
        AngularPhysicsComponent(
            torque=200.0,
            max_angular_velocity=150.0,
        ),
        PlayerLinearMovementInputComponent(),
        PlayerAngularMovementInputComponent(),
        PlayerComponent(),
    ]
    processors = [
        PlayerLinearMovementInputProcessor,
        PlayerAngularMovementInputProcessor,
    ]
