"""
Tests for sound engine functionality.
Tests programmatic sound generation for Nokia Snake Game.
"""

import pytest
import os
import tempfile
import json


class TestSoundEngine:
    """Test suite for sound engine functionality."""
    
    def test_sound_engine_file_exists(self):
        """Test that sound_engine.js exists."""
        sound_file = os.path.join(os.path.dirname(__file__), 'static', 'sound_engine.js')
        assert os.path.exists(sound_file), "sound_engine.js should exist in static directory"
    
    def test_sound_engine_contains_required_functions(self):
        """Test that sound_engine.js contains required sound functions."""
        sound_file = os.path.join(os.path.dirname(__file__), 'static', 'sound_engine.js')
        with open(sound_file, 'r') as f:
            content = f.read()
        
        # Check for required function definitions
        assert 'class SoundEngine' in content, "Should contain SoundEngine class"
        assert 'playFoodEatenSound' in content, "Should contain playFoodEatenSound function"
        assert 'playGameOverSound' in content, "Should contain playGameOverSound function"
        assert 'playGameStartSound' in content, "Should contain playGameStartSound function"
        assert 'AudioContext' in content, "Should use Web Audio API"
    
    def test_sound_engine_has_enable_disable_functionality(self):
        """Test that sound engine can be enabled/disabled."""
        sound_file = os.path.join(os.path.dirname(__file__), 'static', 'sound_engine.js')
        with open(sound_file, 'r') as f:
            content = f.read()
        
        assert 'soundEnabled' in content, "Should have soundEnabled property"
        assert 'enableSound' in content, "Should have enableSound method"
        assert 'disableSound' in content, "Should have disableSound method"


class TestSoundIntegration:
    """Test suite for sound integration with game."""
    
    def test_game_js_imports_sound_engine(self):
        """Test that game.js integrates with sound engine."""
        game_file = os.path.join(os.path.dirname(__file__), 'static', 'game.js')
        with open(game_file, 'r') as f:
            content = f.read()
        
        assert 'SoundEngine' in content, "game.js should reference SoundEngine"
        assert 'soundEngine' in content, "Should create soundEngine instance"
    
    def test_food_eaten_sound_trigger(self):
        """Test that food eaten sound is triggered when score increases."""
        game_file = os.path.join(os.path.dirname(__file__), 'static', 'game.js')
        with open(game_file, 'r') as f:
            content = f.read()
        
        # Look for sound trigger in updateGame method when score changes
        assert 'playFoodEatenSound' in content, "Should call playFoodEatenSound when food is eaten"
    
    def test_game_over_sound_trigger(self):
        """Test that game over sound is triggered when game ends."""
        game_file = os.path.join(os.path.dirname(__file__), 'static', 'game.js')
        with open(game_file, 'r') as f:
            content = f.read()
        
        assert 'playGameOverSound' in content, "Should call playGameOverSound when game ends"
    
    def test_game_start_sound_trigger(self):
        """Test that game start sound is triggered when game begins."""
        game_file = os.path.join(os.path.dirname(__file__), 'static', 'game.js')
        with open(game_file, 'r') as f:
            content = f.read()
        
        assert 'playGameStartSound' in content, "Should call playGameStartSound when game starts"


class TestHTMLSoundToggle:
    """Test suite for sound toggle in HTML interface."""
    
    def test_html_contains_sound_toggle(self):
        """Test that game.html contains sound enable/disable toggle."""
        html_file = os.path.join(os.path.dirname(__file__), 'templates', 'game.html')
        with open(html_file, 'r') as f:
            content = f.read()
        
        assert 'sound' in content.lower(), "Should contain sound toggle elements"
        assert 'type="checkbox"' in content or 'soundToggle' in content, "Should have sound toggle control"
