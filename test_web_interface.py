"""
Test suite for the Flask web interface.
Tests that the web routes serve the correct templates and handle game interactions.
"""

import pytest
import json
from app import app


class TestGameRoutes:
    """Test Flask routes for the game interface."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_home_route_renders_template(self, client):
        """Test that home route renders the correct template."""
        response = client.get('/')
        assert response.status_code == 200
        # Should contain Nokia-style content
        assert b'Nokia' in response.data or b'Snake' in response.data
    
    def test_game_route_renders_game_template(self, client):
        """Test that game route renders the game template."""
        response = client.get('/game')
        assert response.status_code == 200
        # Should contain canvas element for game rendering
        assert b'canvas' in response.data
        # Should contain Nokia-style styling
        assert b'monochrome' in response.data or b'nokia' in response.data.lower()
    
    def test_game_template_has_required_elements(self, client):
        """Test that game template contains all required HTML elements."""
        response = client.get('/game')
        assert response.status_code == 200
        
        # Game canvas
        assert b'<canvas' in response.data
        assert b'id="gameCanvas"' in response.data
        
        # Score display
        assert b'score' in response.data.lower()
        
        # Game controls information
        assert b'arrow' in response.data.lower() or b'wasd' in response.data.lower()


class TestGameAPI:
    """Test API endpoints for game state management."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_new_game_endpoint(self, client):
        """Test that new game endpoint creates a fresh game."""
        response = client.post('/api/game/new')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'snake' in data
        assert 'food' in data
        assert 'score' in data
        assert 'state' in data
        assert data['score'] == 0
        assert data['state'] == 'ready'
    
    def test_game_state_endpoint(self, client):
        """Test that game state endpoint returns current game state."""
        # First create a new game
        client.post('/api/game/new')
        
        # Then get the state
        response = client.get('/api/game/state')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'snake' in data
        assert 'food' in data
        assert 'score' in data
        assert 'state' in data
    
    def test_move_endpoint(self, client):
        """Test that move endpoint handles direction changes."""
        # Create new game and start it
        client.post('/api/game/new')
        client.post('/api/game/start')
        
        # Test direction change
        response = client.post('/api/game/move', 
                             json={'direction': 'up'})
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True
    
    def test_start_game_endpoint(self, client):
        """Test that start endpoint changes game state to playing."""
        # Create new game
        client.post('/api/game/new')
        
        # Start the game
        response = client.post('/api/game/start')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['state'] == 'playing'
    
    def test_game_update_endpoint(self, client):
        """Test that update endpoint processes game tick."""
        # Create and start game
        client.post('/api/game/new')
        client.post('/api/game/start')
        
        # Update game (move snake)
        response = client.post('/api/game/update')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'snake' in data
        assert 'food' in data
        assert 'score' in data
        assert 'state' in data


class TestNokiaStyleInterface:
    """Test Nokia 1100-specific styling and layout."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_css_contains_monochrome_styling(self, client):
        """Test that CSS file contains Nokia-style monochrome colors."""
        response = client.get('/static/style.css')
        assert response.status_code == 200
        
        css_content = response.data.decode('utf-8').lower()
        # Should contain monochrome colors (black/green/dark colors)
        assert '#000' in css_content or 'black' in css_content
        assert ('#0f0' in css_content or '#00ff00' in css_content or 
                'green' in css_content or '#090' in css_content)
    
    def test_game_has_nokia_dimensions(self, client):
        """Test that game canvas has Nokia-appropriate dimensions."""
        response = client.get('/game')
        assert response.status_code == 200
        
        # Should specify canvas dimensions suitable for Nokia screen
        content = response.data.decode('utf-8')
        assert 'width=' in content and 'height=' in content
    
    def test_game_displays_high_score(self, client):
        """Test that game interface shows high score feature."""
        response = client.get('/game')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8').lower()
        assert 'high' in content or 'best' in content or 'record' in content
    
    def test_retro_font_styling(self, client):
        """Test that interface uses retro/pixel-style fonts."""
        response = client.get('/static/style.css')
        assert response.status_code == 200
        
        css_content = response.data.decode('utf-8').lower()
        # Should use monospace or pixel-style fonts
        assert ('monospace' in css_content or 'courier' in css_content or 
                'pixel' in css_content or 'retro' in css_content)
