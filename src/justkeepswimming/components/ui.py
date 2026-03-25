from dataclasses import dataclass, field

from pygame import Color
from justkeepswimming.ecs import Component
from justkeepswimming.utilities.signal import Signal


@dataclass
class ButtonComponent(Component):
    label_color: Color = field(default_factory=lambda: Color(255, 255, 255))
    label_color_hover: Color = field(default_factory=lambda: Color(200, 200, 200))
    background_color: Color = field(default_factory=lambda: Color(0, 0, 0))
    hover_background_color: Color = field(default_factory=lambda: Color(50, 50, 50))
    is_hovered: bool = False

    on_click: Signal[[]] = field(default_factory=Signal)
    on_release: Signal[[]] = field(default_factory=Signal)
    on_hover: Signal[[]] = field(default_factory=Signal)
    on_unhover: Signal[[]] = field(default_factory=Signal)
