# List all debug processors here so they can be automatically registered when a scene is entered
from justkeepswimming.debug.processors.rendering import (
    RendererDebuggerProcessor,
)
from justkeepswimming.debug.processors.rendering import MouseDebuggerProcessor
from justkeepswimming.debug.processors.physics import (
    LinearPhysicsDebuggerProcessor,
)
from justkeepswimming.debug.processors.button import ButtonDebuggerProcessor

__all__ = [
    "RendererDebuggerProcessor",
    "MouseDebuggerProcessor",
    "LinearPhysicsDebuggerProcessor",
    "ButtonDebuggerProcessor",
]
