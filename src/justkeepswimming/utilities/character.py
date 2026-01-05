from dataclasses import dataclass

from justkeepswimming.utilities.animation import Spritesheet


@dataclass(frozen=True)
class Character:
    spritesheet: Spritesheet
