from dataclasses import dataclass, field
import logging

from pygame import Color
from justkeepswimming.ecs import Component
from justkeepswimming.utilities.signal import Signal

logger = logging.getLogger(__name__)

@dataclass
class ButtonComponent(Component):
    label_color: Color = field(default_factory=lambda: Color(255, 255, 255))
    background_color: Color = field(default_factory=lambda: Color(0, 0, 0))
    label_color_hover: Color = field(default_factory=lambda: Color(200, 200, 200))
    background_color_hover: Color = field(default_factory=lambda: Color(50, 50, 50))
    label_color_active: Color = field(default_factory=lambda: Color(237, 235, 235))
    background_color_active: Color = field(default_factory=lambda: Color(15, 15, 15))
    active: bool = False
    hovering: bool = False

    on_click: Signal[[]] = field(default_factory=Signal)
    on_release: Signal[[]] = field(default_factory=Signal)
    on_hover: Signal[[]] = field(default_factory=Signal)
    on_unhover: Signal[[]] = field(default_factory=Signal)
