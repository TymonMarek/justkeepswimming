from dataclasses import dataclass, field

from pygame import Vector2

from justkeepswimming.ecs import Component


@dataclass
class TransformComponent(Component):
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    rotation: float = 0.0
    size: Vector2 = field(default_factory=lambda: Vector2(1, 1))
    anchor: Vector2 = field(default_factory=lambda: Vector2(0.5, 0.5))

    @property
    def up(self) -> Vector2:
        return Vector2(0, -1).rotate(self.rotation)

    @property
    def right(self) -> Vector2:
        return Vector2(1, 0).rotate(self.rotation)
