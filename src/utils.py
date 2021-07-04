from typing import Optional


class Point:
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

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __lt__(self, other):
        if self.x < other and self.y < other:
            return True
        else:
            return False

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        if self.direction is None:
            return f"Point(x={self.x}, y={self.y})"
        else:
            return f"Point(x={self.x}, y={self.y}, dir={self.direction})"
