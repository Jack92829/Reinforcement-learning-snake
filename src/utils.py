from typing import Optional, Union


class Point:
    """Objects representing a particular position on a grid, may represent vector or scalar points"""
    __slots__ = ("x", "y", "direction")

    def __init__(
        self,
        x: int,
        y: int,
        direction: Optional[str] = None
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction

    @property
    def left(self):  # The point to the immediate left of self
        return Point(self.x - 1, self.y, self.direction)

    @property
    def right(self):  # The point to the immediate right of self
        return Point(self.x + 1, self.y, self.direction)

    @property
    def up(self):  # The point immediately above self
        return Point(self.x, self.y + 1, self.direction)

    @property
    def down(self):  # The point immediately below self
        return Point(self.x, self.y - 1, self.direction)

    def copy(self):
        return Point(self.x, self.y, self.direction)

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __lt__(self, other) -> bool:
        if self.x < other and self.y < other:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        if self.x > other and self.y > other:
            return True
        else:
            return False

    def __add__(self, other: Union["Point", "Slope"]) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self) -> str:
        if self.direction is None:
            return f"Point(x={self.x}, y={self.y})"
        else:
            return f"Point(x={self.x}, y={self.y}, dir={self.direction})"


class Slope:
    """Objects storing a gradient, used to travel along a line of sight"""
    __slots__ = ("x", "y")

    def __init__(self, rise, run) -> None:
        self.x = rise
        self.y = run


class LineOfSight:
    __slots__ = ("apple", "snake", "wall")

    def __init__(self) -> None:
        self.apple = None
        self.snake = None
        self.wall = 0

    def __contains__(self, other) -> bool:
        ...


VISION_TYPES = {
    4: (
        Slope(1, 0),
        Slope(0, -1),
        Slope(0, -1),
        Slope(1, 0)
    ),
    8: (
        Slope(1, -1),  # Left-up
        Slope(1, 0),  # Up
        Slope(1, 1),  # Right-up
        Slope(0, -1),  # Left
        Slope(0, 1),  # Right
        Slope(-1, -1),  # Left-down
        Slope(-1, 0),  # Down
        Slope(-1, 1)  # Right-down
    )
}
