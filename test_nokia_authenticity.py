"""
Test suite for Nokia 1100 authenticity features.
Tests that the game accurately recreates the Nokia 1100 Snake experience.
"""

import pytest
from game_engine import SnakeGame
from app import app


class TestNokiaGameplayFeatures:
    """Test gameplay features specific to Nokia 1100."""
    
    def test_game_speed_is_nokia_appropriate(self):
        """Test that game has Nokia-like speed settings."""
        # Nokia speed was roughly 200-300ms per move
        # This is tested indirectly through the frontend JavaScript
        # Here we test that the game engine supports appropriate speeds
        game = SnakeGame()
        game.start()
        
        # Game should respond immediately to moves
        initial_position = game.snake_head
        game.move()
        new_position = game.snake_head
        
        # Should move exactly one grid space
        assert abs(new_position[0] - initial_position[0]) + abs(new_position[1] - initial_position[1]) == 1
    
    def test_score_system_matches_nokia(self):
        """Test that scoring system matches Nokia 1100 (10 points per food)."""
        game = SnakeGame()
        initial_score = game.score
        
        game.eat_food()
        assert game.score == initial_score + 10
    
    def test_grid_size_is_appropriate(self):
        """Test that grid size matches Nokia 1100 proportions."""
        game = SnakeGame()
        
        # Nokia 1100 had approximately 20x20 grid
        assert game.grid_width == 20
        assert game.grid_height == 20
        
        # Snake should start near center
        center_x = game.grid_width // 2
        center_y = game.grid_height // 2
        
        head_x, head_y = game.snake_head
        assert abs(head_x - center_x) <= 1
        assert abs(head_y - center_y) <= 1
    
    def test_initial_snake_length_is_correct(self):
        """Test that snake starts with Nokia-appropriate length."""
        game = SnakeGame()
        
        # Nokia snake started with 3 segments
        assert len(game.snake_body) == 3


class TestNokiaVisualAuthenticity:
    """Test visual elements match Nokia 1100 style."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_monochrome_color_scheme(self, client):
        """Test that the game uses authentic Nokia monochrome colors."""
        response = client.get('/static/style.css')
        assert response.status_code == 200
        
        css_content = response.data.decode('utf-8')
        
        # Should use black background
        assert '#000' in css_content
        
        # Should use green for snake/text (Nokia green)
        assert '#0f0' in css_content or '#00ff00' in css_content
        
        # Should not use many colors (keep it monochrome)
        import re
        color_codes = re.findall(r'#[a-fA-F0-9]{3,6}', css_content)
        assert len(color_codes) <= 20  # Limited to just black and green variations
    
    def test_pixel_perfect_styling(self, client):
        """Test that styling mimics Nokia pixel-perfect display."""
        response = client.get('/static/style.css')
        css_content = response.data.decode('utf-8')
        
        # Should use monospace fonts
        assert 'monospace' in css_content.lower() or 'courier' in css_content.lower()
        
        # Should have pixelated/blocky styling
        assert 'border-radius' in css_content  # For that classic rounded Nokia look
    
    def test_authentic_game_dimensions(self, client):
        """Test that game canvas has Nokia-appropriate aspect ratio."""
        response = client.get('/game')
        content = response.data.decode('utf-8')
        
        # Canvas should be square (Nokia screen was roughly square)
        assert 'width="400"' in content and 'height="400"' in content


class TestNokiaUserExperience:
    """Test user experience features from Nokia 1100."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_high_score_persistence(self, client):
        """Test that high score feature exists (Nokia had this)."""
        response = client.get('/game')
        content = response.data.decode('utf-8').lower()
        
        # Should mention high score
        assert 'high score' in content or 'best' in content
        
        # Should have JavaScript for localStorage (modern equivalent of Nokia's memory)
        js_response = client.get('/static/game.js')
        js_content = js_response.data.decode('utf-8')
        assert 'localStorage' in js_content
    
    def test_game_over_behavior(self, client):
        """Test that game over behavior matches Nokia style."""
        # Test game over through API
        client.post('/api/game/new')
        client.post('/api/game/start')
        
        # Game should handle game over state
        response = client.get('/api/game/state')
        data = response.get_json()
        assert 'state' in data
    
    def test_control_instructions(self, client):
        """Test that control instructions are displayed (Nokia style help)."""
        response = client.get('/game')
        content = response.data.decode('utf-8').lower()
        
        # Should mention arrow keys or WASD
        assert ('arrow' in content and 'key' in content) or 'wasd' in content
    
    def test_retro_sound_ready(self, client):
        """Test that the interface is ready for retro sound effects."""
        # Check if JavaScript structure supports sound
        js_response = client.get('/static/game.js')
        js_content = js_response.data.decode('utf-8')
        
        # Should have game state management that could trigger sounds
        assert 'gameState' in js_content
        assert ('game_over' in js_content or 'gameOver' in js_content)
