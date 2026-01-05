from dataclasses import dataclass, field

from pygame import Vector2


@dataclass
class Transform:
    position: Vector2
    rotation: float
    size: Vector2
    anchor: Vector2 = field(default_factory=lambda: Vector2(0, 0))


class Grid:
    def __init__(
        self,
        rows: int,
        columns: int,
        cell_size: Vector2,
        origin: Vector2 = Vector2(0, 0),
    ):
        self.origin = origin
        self.cell_size = cell_size
        self.rows = rows
        self.columns = columns

    def cell(self, row: int, column: int) -> Transform:
        if column < 0 or column >= self.columns:
            raise IndexError(f"column {column} out of range")
        if row < 0 or row >= self.rows:
            raise IndexError(f"row {row} out of range")

        position = Vector2(
            self.origin.x + column * self.cell_size.x,
            self.origin.y + row * self.cell_size.y,
        )

        return Transform(position, 0, self.cell_size)
