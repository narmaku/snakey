"""
Nokia 1100 Snake Game Engine
Core game mechanics for the classic snake game.
"""

from enum import Enum
import random
from typing import List, Tuple, Optional


class Direction(Enum):
    """Direction enumeration for snake movement."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class GameState(Enum):
    """Game state enumeration."""
    READY = "ready"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class SnakeGame:
    """Nokia 1100 Snake Game Engine."""
    
    def __init__(self, grid_width: int = 20, grid_height: int = 20):
        """Initialize the game with default Nokia 1100 settings."""
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # Game state
        self.state = GameState.READY
        self.score = 0
        self.direction = Direction.RIGHT
        
        # Snake initialization - starts at center
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        
        # Snake body: head is first element, tail is last
        self.snake_body = [
            (center_x, center_y),      # head
            (center_x - 1, center_y),  # body
            (center_x - 2, center_y)   # tail
        ]
        
        # Generate initial food
        self.food_position = self._generate_food()
    
    @property
    def snake_head(self) -> Tuple[int, int]:
        """Get the snake's head position."""
        return self.snake_body[0]
    
    def _generate_food(self) -> Tuple[int, int]:
        """Generate food at random position not occupied by snake."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            food_pos = (x, y)
            
            # Ensure food doesn't spawn on snake
            if food_pos not in self.snake_body:
                return food_pos
    
    def change_direction(self, new_direction: Direction):
        """Change snake's direction if valid."""
        # Prevent reversing direction (can't go backward)
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction
    
    def move(self):
        """Move snake one step in current direction."""
        head_x, head_y = self.snake_head
        
        # Calculate new head position
        direction_deltas = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0)
        }
        
        dx, dy = direction_deltas[self.direction]
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.snake_body.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food_position:
            self.eat_food()
        else:
            # Remove tail if no food eaten (normal movement)
            self.snake_body.pop()
    
    def eat_food(self):
        """Handle food consumption."""
        self.score += 10
        self.food_position = self._generate_food()
        # Note: snake body already grew when new head was added in move()
    
    def check_collision(self) -> bool:
        """Check if snake collided with wall or itself."""
        head_x, head_y = self.snake_head
        
        # Wall collision
        if (head_x < 0 or head_x >= self.grid_width or 
            head_y < 0 or head_y >= self.grid_height):
            return True
        
        # Self collision (head hits body)
        if self.snake_head in self.snake_body[1:]:
            return True
        
        return False
    
    def start(self):
        """Start the game."""
        self.state = GameState.PLAYING
    
    def update(self):
        """Update game state (check for game over conditions)."""
        if self.state == GameState.PLAYING and self.check_collision():
            self.state = GameState.GAME_OVER
    
    def restart(self):
        """Restart the game to initial state."""
        self.__init__(self.grid_width, self.grid_height)
