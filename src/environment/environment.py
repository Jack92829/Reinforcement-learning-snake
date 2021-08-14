import logging
from math import hypot
from typing import Union

from utils import Point
from environment.snake import Snake
from environment.apple import Apple
from __main__ import constants

REWARDS = constants.Environment.Rewards
VISION = constants.Environment.Vision

logger = logging.getLogger(__name__)


class Environment:
    def __init__(
        self,
        grid_size: int,
        apple_position: list[int],
        snake_position: list[list[int]]
    ) -> None:
        self.grid_size = grid_size
        self.apple = Apple(*apple_position, grid_size)
        self.snake = Snake(grid_size, VISION.type, VISION.directions, snake_position)

        logger.info("Successfully initialised an instance of class Environment")

    @property
    def state(self) -> list[Union[int, float]]:
        """Produces a state_list that can be fed to a neural network"""
        state_list = []
        direction_mapping = {
            "left": [1, 0, 0, 0],
            "right": [0, 1, 0, 0],
            "up": [0, 0, 1, 0],
            "down": [0, 0, 0, 1]
        }

        for line_of_sight in self.snake.view_surroundings(self.apple):
            state_list.extend(line_of_sight)

        state_list.extend(direction_mapping[self.snake.direction])
        return state_list

    def perform_action(self, action: int) -> None:
        """Perform the action determined by the agent"""
        directions = ('u', 'l', 'd', 'r')
        current_direction = self.snake.direction

        if action == 0:  # Turn left
            self.snake.direction = directions[directions.index(current_direction) - 3]
        elif action == 2:  # Turn right
            self.snake.direction = directions[directions.index(current_direction) - 1]
        # Otherwise, continue straight forwards

    def step(self) -> ...:
        """Perform a timestep, updating the environment"""
        reward = 0

        if self.snake.has_died():
            reward += REWARDS.death
            self.reset()

            logger.debug("Snake has died")
            return ...

        # Update the snakes position
        if REWARDS.towards_apple or REWARDS.away_from_apple:
            distance_before = self.find_distance_to(self.apple.position)
            self.snake.update_positions()
            distance_after = self.find_distance_to(self.apple.position)

            if distance_after <= distance_before:  # Reward if it moved towards the apple
                reward += REWARDS.towards_apple
            else:   # Reward if it moved away from the apple
                reward += REWARDS.away_from_apple
        else:
            self.snake.update_positions()

        if self.snake.has_eaten(self.apple):
            reward += REWARDS.apple
            self.apple.change_position(self.snake)

        reward += REWARDS.timestep

        logger.debug(f"Completed a timestep with a reward of {reward}")

    def find_distance_to(self, other: Point) -> float:
        """Calculate the distance between the apple and another point"""
        return hypot(self.apple.x - other.x, self.apple.y - other.y)

    def reset(self) -> None:
        """Reset the environment back to its initial state"""
        self.snake.reset()
        self.apple.change_position(self.snake)

logger.debug("testing this")