from justkeepswimming.characters.turtle import TurtlePrefab
from justkeepswimming.components.input import PlayerMovementInputComponent
from justkeepswimming.processors.input import PlayerMovementInputProcessor
from justkeepswimming.utilities.prefab import Prefab


class PlayerPrefab(Prefab):
    extends = TurtlePrefab()
    components = [PlayerMovementInputComponent()]
    processors = [PlayerMovementInputProcessor]
