from dataclasses import dataclass
from enum import Enum, auto
import pygame

from justkeepswimming.debug.profiler import Profiler
from justkeepswimming.systems.clock import Clock
from justkeepswimming.systems.dispatcher import Dispatcher
from justkeepswimming.systems.input import Input
from justkeepswimming.systems.window import Window
from justkeepswimming.utilities.custom_event import CustomEvent
from justkeepswimming.utilities.launch import Options

pygame.font.init()


class CustomEventType(Enum):
    QUIT = auto()


@dataclass(frozen=True)
class EngineContext:
    clock: Clock
    window: Window
    dispatcher: Dispatcher
    input: Input
    profiler: Profiler
    options: Options
    custom_events: dict[CustomEventType, CustomEvent]
