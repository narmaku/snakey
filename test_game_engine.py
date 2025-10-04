"""
Test suite for the Snake game engine.
Tests core game mechanics: snake movement, food generation, collision detection, scoring.
"""

import pytest
from game_engine import SnakeGame, Direction, GameState


class TestSnakeGameInitialization:
    """Test game initialization and initial state."""
    
    def test_game_creates_successfully(self):
        """Test that a new game can be created."""
        game = SnakeGame()
        assert game is not None
    
    def test_initial_game_state_is_ready(self):
        """Test that new game starts in READY state."""
        game = SnakeGame()
        assert game.state == GameState.READY
    
    def test_initial_score_is_zero(self):
        """Test that new game starts with score of 0."""
        game = SnakeGame()
        assert game.score == 0
    
    def test_initial_snake_has_correct_position(self):
        """Test that snake starts at center of grid."""
        game = SnakeGame()
        # Default grid should be 20x20, snake starts at (10, 10)
        expected_head = (10, 10)
        assert game.snake_head == expected_head
    
    def test_initial_snake_length(self):
        """Test that snake starts with length 3."""
        game = SnakeGame()
        assert len(game.snake_body) == 3
    
    def test_initial_direction_is_right(self):
        """Test that snake initially moves right."""
        game = SnakeGame()
        assert game.direction == Direction.RIGHT
    
    def test_food_is_generated_initially(self):
        """Test that food is placed on the grid initially."""
        game = SnakeGame()
        assert game.food_position is not None
        assert len(game.food_position) == 2  # (x, y) coordinates


class TestSnakeMovement:
    """Test snake movement mechanics."""
    
    def test_snake_moves_right(self):
        """Test that snake moves right correctly."""
        game = SnakeGame()
        initial_head = game.snake_head
        game.move()
        
        new_head = game.snake_head
        assert new_head[0] == initial_head[0] + 1  # x increased by 1
        assert new_head[1] == initial_head[1]      # y unchanged
    
    def test_snake_can_change_direction_up(self):
        """Test that snake can change direction to up."""
        game = SnakeGame()
        game.change_direction(Direction.UP)
        assert game.direction == Direction.UP
        
        initial_head = game.snake_head
        game.move()
        new_head = game.snake_head
        assert new_head[1] == initial_head[1] - 1  # y decreased by 1
        assert new_head[0] == initial_head[0]      # x unchanged
    
    def test_snake_can_change_direction_down(self):
        """Test that snake can change direction to down."""
        game = SnakeGame()
        game.change_direction(Direction.DOWN)
        assert game.direction == Direction.DOWN
        
        initial_head = game.snake_head
        game.move()
        new_head = game.snake_head
        assert new_head[1] == initial_head[1] + 1  # y increased by 1
        assert new_head[0] == initial_head[0]      # x unchanged
    
    def test_snake_can_change_direction_left(self):
        """Test that snake can change direction to left."""
        game = SnakeGame()
        # First change to UP to avoid reverse direction issue
        game.change_direction(Direction.UP)
        game.move()  # Move up first
        
        # Now we can change to LEFT
        game.change_direction(Direction.LEFT)
        assert game.direction == Direction.LEFT
        
        initial_head = game.snake_head
        game.move()
        new_head = game.snake_head
        assert new_head[0] == initial_head[0] - 1  # x decreased by 1
        assert new_head[1] == initial_head[1]      # y unchanged
    
    def test_snake_cannot_reverse_direction(self):
        """Test that snake cannot move directly backwards."""
        game = SnakeGame()
        # Snake starts moving right, should not be able to go left
        game.change_direction(Direction.LEFT)
        assert game.direction == Direction.RIGHT  # Should stay right


class TestFoodAndGrowth:
    """Test food mechanics and snake growth."""
    
    def test_snake_grows_when_eating_food(self):
        """Test that snake length increases when eating food."""
        game = SnakeGame()
        initial_length = len(game.snake_body)
        
        # Position snake head next to food, then move to eat it
        food_x, food_y = game.food_position
        game.snake_body[0] = (food_x - 1, food_y)  # Position head next to food
        game.direction = Direction.RIGHT  # Move toward food
        
        game.move()  # This should eat the food and grow the snake
        
        assert len(game.snake_body) == initial_length + 1
    
    def test_score_increases_when_eating_food(self):
        """Test that score increases by 10 when eating food."""
        game = SnakeGame()
        initial_score = game.score
        
        game.eat_food()
        assert game.score == initial_score + 10
    
    def test_new_food_generated_after_eating(self):
        """Test that new food appears after eating current food."""
        game = SnakeGame()
        old_food_position = game.food_position
        
        game.eat_food()
        assert game.food_position != old_food_position
        assert game.food_position is not None


class TestCollisionDetection:
    """Test collision detection mechanics."""
    
    def test_wall_collision_detection_right(self):
        """Test collision with right wall."""
        game = SnakeGame()
        # Move snake to right edge
        game.snake_body[0] = (19, 10)  # x=19 is right edge for 20x20 grid
        game.direction = Direction.RIGHT
        game.move()
        
        assert game.check_collision() is True
    
    def test_wall_collision_detection_left(self):
        """Test collision with left wall."""
        game = SnakeGame()
        # Move snake to left edge
        game.snake_body[0] = (0, 10)
        game.direction = Direction.LEFT
        game.move()
        
        assert game.check_collision() is True
    
    def test_wall_collision_detection_top(self):
        """Test collision with top wall."""
        game = SnakeGame()
        # Move snake to top edge
        game.snake_body[0] = (10, 0)
        game.direction = Direction.UP
        game.move()
        
        assert game.check_collision() is True
    
    def test_wall_collision_detection_bottom(self):
        """Test collision with bottom wall."""
        game = SnakeGame()
        # Move snake to bottom edge
        game.snake_body[0] = (10, 19)
        game.direction = Direction.DOWN
        game.move()
        
        assert game.check_collision() is True
    
    def test_self_collision_detection(self):
        """Test collision with snake's own body."""
        game = SnakeGame()
        # Create a longer snake that can collide with itself
        game.snake_body = [(5, 5), (4, 5), (3, 5), (3, 6), (4, 6), (5, 6)]
        # Move head to collide with body
        game.snake_body[0] = (4, 6)  # Same position as a body segment
        
        assert game.check_collision() is True
    
    def test_no_collision_in_normal_movement(self):
        """Test that no collision occurs during normal movement."""
        game = SnakeGame()
        game.move()  # Normal move
        assert game.check_collision() is False


class TestGameState:
    """Test game state management."""
    
    def test_game_starts(self):
        """Test that game can be started."""
        game = SnakeGame()
        game.start()
        assert game.state == GameState.PLAYING
    
    def test_game_ends_on_collision(self):
        """Test that game ends when collision occurs."""
        game = SnakeGame()
        game.start()
        
        # Force collision
        game.snake_body[0] = (20, 10)  # Out of bounds
        game.move()
        game.update()
        
        assert game.state == GameState.GAME_OVER
    
    def test_game_can_be_restarted(self):
        """Test that game can be restarted after game over."""
        game = SnakeGame()
        game.start()
        
        # End game
        game.state = GameState.GAME_OVER
        
        # Restart
        game.restart()
        assert game.state == GameState.READY
        assert game.score == 0
        assert len(game.snake_body) == 3
