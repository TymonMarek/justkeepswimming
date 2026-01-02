from dataclasses import dataclass

from src.modules.clock import Clock
from src.modules.window import Window
from src.modules.dispatcher import Dispatcher


@dataclass(frozen=True)
class GameContext:
    clock: Clock
    window: Window
    dispatcher: Dispatcher
