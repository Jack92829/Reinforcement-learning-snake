import logging
from collections import deque
from typing import TYPE_CHECKING

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
            logging.critial("Failed to find vision type of value {vision}", exc_info=True)
            raise err

        logging.info("Successfully initialised an instance of class Snake")

    def update_positions(self) -> None:
        """I really want to call it 'slither'"""
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
    
    def view_surroundings(self, apple: "Apple"):
        head = self.positions[0]

        for gradient in self.vision_type:
            ...
    
    def _view_direction(self, gradient: Slope, apple_position: Point) -> tuple[int, int]:
        # We don't want to start on the head
        position = self.positions[0] + gradient

        apple_found = False
        body_found = False

        steps = 0

        while position < self.grid_size:
            if position == apple_position:
                apple_found = True
                distance_to_apple = steps / (len(self.grid_size) - 1)

            if not body_found and position in self.positions:
                body_found = True
                distance_to_self = steps / (len(self.grid_size) - 1)

            position += gradient
            steps += 1

        distance_to_wall = steps / (len(self.grid_size) - 1)

        if self.vision_type == "binary":
            return (apple_found, body_found, distance_to_wall)
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
