import logging
from typing import TYPE_CHECKING
from random import randrange

from utils import Point

if TYPE_CHECKING:
    from snake import Snake

logger = logging.getLogger(__name__)


class Apple:
    __slots__ = ("position", "starting_position", "grid_size")

    def __init__(self, x: int, y: int, grid_size: int) -> None:
        self.position = Point(x, y)
        self.starting_position = Point(x, y)
        self.grid_size = grid_size

        logging.info("Successfully initialised an instance of class Apple")

    def change_position(self, snake: Snake) -> None:
        while True:
            x = randrange(0, self.grid_size)
            y = randrange(0, self.grid_size)

            if (x, y) not in snake:
                break

        self.position = Point(x, y)

    def reset(self) -> None:
        self.position = self.starting_position

    def __str__(self) -> str:
        return f"Apple(position={self.position})"
