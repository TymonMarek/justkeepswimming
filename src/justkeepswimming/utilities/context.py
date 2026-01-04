from dataclasses import dataclass

from justkeepswimming.modules.clock import Clock
from justkeepswimming.modules.dispatcher import Dispatcher
from justkeepswimming.modules.window import Window


@dataclass(frozen=True)
class GameContext:
    clock: Clock
    window: Window
    dispatcher: Dispatcher
