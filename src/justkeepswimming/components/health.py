from dataclasses import dataclass, field

from justkeepswimming.ecs import Component
from justkeepswimming.utilities.signal import Signal


@dataclass
class HealthComponent(Component):
    current_health: float = 100.0
    max_health: float = 100.0
    is_invincible: bool = False
    is_alive: bool = True
    on_died: Signal[[]] = field(default_factory=Signal[[]])
