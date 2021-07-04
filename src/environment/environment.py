from math import hypot

from utils import Point
from environment.snake import Snake
from environment.apple import Apple
import __main__.constants.Environment.Rewards as REWARDS


class Environment:
    def __init__(self, grid_size: int, apple: Apple, snake: Snake) -> None:
        self.grid_size = grid_size
        self.apple = apple
        self.snake = snake

    def perform_action(self, action: int) -> None:
        """Perform the action determined by the agent"""
        directions = ('u', 'l', 'd', 'r')
        current_direction = self.snake.direction

        if action == 0:  # Turn left
            self.snake.direction = directions[directions.index(current_direction) - 3]
        elif action == 1:  # Continue straight
            return
        elif action == 2:  # Turn right
            self.snake.direction = directions[directions.index(current_direction) - 1]

    def step(self):
        """Perform a timestep, updating the environment"""
        reward = 0

        if self.snake.has_died():
            reward += REWARDS.death
            self.reset()

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

    def find_distance_to(self, other: Point) -> float:
        """Calculate the distance between the apple and another point"""
        return hypot(self.apple.x - other.x, self.apple.y - other.y)

    def reset(self) -> None:
        """Reset the environment back to its initial state"""
        self.snake.reset()
        self.apple.change_position(self.snake)
