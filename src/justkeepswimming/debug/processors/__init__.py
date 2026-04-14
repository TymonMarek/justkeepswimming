"""
This module contains all of the debugger processors that can be used in the
debug build of the engine. These processors are meant to be used for debugging
purposes and may have performance implications, so they should not be included
in the release build of the engine.
"""
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
