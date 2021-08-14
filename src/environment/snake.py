import logging
from collections import deque
from typing import TYPE_CHECKING, Generator

from utils import Point, Slope, VISION_TYPES
from __main__ import constants

VISION = constants.Environment.vision

if TYPE_CHECKING:
    from apple import Apple

logger = logging.getLogger(__name__)


class Snake:
    __slots__ = ("grid_size", "positions", "starting_positions", "direction", "vision", "vision_type")

    def __init__(
        self,
        grid_size: int,
        vision_type: str,
        vision_magnitude: int,
        positions: list[tuple[int, int]]
    ) -> None:
        self.grid_size: int = grid_size
        self.positions: deque[Point] = deque([Point(*pos, 'right') for pos in positions])
        self.starting_positions: deque[Point] = self.positions.copy()

        self.direction = "right"

        self.vision_type = vision_type
        try:
            self.vision = VISION_TYPES[vision_magnitude]
        except KeyError as err:
            logging.critial("Failed to find vision of magnitude {vision_magnitude}", exc_info=True)
            raise err

        logging.info("Successfully initialised an instance of class Snake")

    def update_positions(self) -> None:
        """Moves the snake in its direction of travel (I really want to call it 'slither')"""
        head = self.positions[0]
        self.positions = self.positions.rotate(1)

        if (direction := self.direction) == "left":
            self.positions[0] = head.left
        elif direction == "right":
            self.positions[0] = head.right
        elif direction == "up":
            self.positions[0] = head.up
        elif direction == "down":
            self.positions[0] = head.down

    def view_surroundings(
        self,
        apple: "Apple"
    ) -> Generator[tuple[float, float, float], None, None]:
        """Yield lines of sight from the snakes head"""
        for gradient in self.vision:
            yield self._view_direction(gradient, apple.position)

    def _view_direction(self, gradient: Slope, apple_position: Point) -> tuple[float, float, float]:
        """Travels along a line of sight and collects information to be used in the state array"""
        position = self.positions[0] + gradient  # We don't want to start on the head
        steps = 1

        apple_found = False
        body_found = False

        # Value decreases the closer we get, 1 signifies it's not in the line of sight
        distance_to_apple = 1.0
        distance_to_self = 1.0

        while position >= 0 and position < self.grid_size:
            if position == apple_position:
                apple_found = True
                distance_to_apple = (steps - 1) / (self.grid_size - 1)

            if not body_found and position in self.positions:
                body_found = True  # Prevent observing further occurences of the snake
                distance_to_self = (steps - 1) / (self.grid_size - 1)

            position += gradient
            steps += 1

        distance_to_wall = (steps - 1) / (self.grid_size - 1)

        if self.vision_type == "binary":
            return (float(apple_found), float(body_found), distance_to_wall)
        elif self.vision_type == "magnitudinous":
            return (distance_to_apple, distance_to_self, distance_to_wall)

    def has_eaten(self, apple: "Apple") -> bool:
        """Returns true if the snake has reached the apple"""
        if self.positions[0] == apple.position:
            self.extend()
            return True
        return False

    def has_died(self) -> bool:
        """Returns true if the snake has collided with a wall or itself"""
        if not self.positions[0] < self.grid_size:
            # Return True if the snakes head has collided with the wall
            return True
        elif self.positions[0] in self.positions[1:]:
            # Return True if the snakes head has collided with its body
            return True

        return False

    def extend(self) -> None:
        """Extend the length of the snake by 1 unit"""
        tail = self.positions[-1]

        if (direction := tail.direction) == "left":
            point = tail.right
        elif direction == "right":
            point = tail.left
        elif direction == "up":
            point = tail.down
        elif direction == "down":
            point = tail.up

        self.positions.append(point)

        logger.debug(f"Extended snake to a length of {len(self.positions)}")

    def reset(self) -> None:
        self.positions = self.starting_positions

        logging.debug("Successfully reset snake")

    def __contains__(self, other) -> bool:
        if other in self.positions:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"Snake(length={len(self.positions)}, direction={self.direction}, vision={len(self.vision_type)})"
