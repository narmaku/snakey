"""
Test suite for project setup verification.
Tests that the basic project structure and Flask app are properly configured.
"""

import pytest
import os
from pathlib import Path


class TestProjectStructure:
    """Test that the project has the correct directory structure."""
    
    def test_project_root_exists(self):
        """Test that the project root directory exists."""
        project_root = Path(__file__).parent
        assert project_root.exists()
        assert project_root.is_dir()
    
    def test_app_file_exists(self):
        """Test that the main Flask application file exists."""
        app_file = Path(__file__).parent / "app.py"
        assert app_file.exists()
        assert app_file.is_file()
    
    def test_templates_directory_exists(self):
        """Test that the templates directory exists for HTML templates."""
        templates_dir = Path(__file__).parent / "templates"
        assert templates_dir.exists()
        assert templates_dir.is_dir()
    
    def test_static_directory_exists(self):
        """Test that the static directory exists for CSS/JS files."""
        static_dir = Path(__file__).parent / "static"
        assert static_dir.exists()
        assert static_dir.is_dir()
    
    def test_requirements_file_exists(self):
        """Test that requirements.txt exists with necessary dependencies."""
        requirements_file = Path(__file__).parent / "requirements.txt"
        assert requirements_file.exists()
        
        with open(requirements_file, 'r') as f:
            content = f.read()
            assert "flask" in content.lower()
            assert "pytest" in content.lower()


class TestFlaskApp:
    """Test that the Flask application can be imported and configured."""
    
    def test_app_can_be_imported(self):
        """Test that the Flask app can be imported without errors."""
        try:
            from app import app
            assert app is not None
        except ImportError:
            pytest.fail("Cannot import Flask app from app.py")
    
    def test_app_is_flask_instance(self):
        """Test that the imported app is a valid Flask instance."""
        from app import app
        from flask import Flask
        assert isinstance(app, Flask)
    
    def test_app_has_basic_config(self):
        """Test that the Flask app has basic configuration."""
        from app import app
        assert app.config is not None
        # Should have debug mode configured
        assert 'DEBUG' in app.config


class TestBasicRoutes:
    """Test that basic Flask routes are working."""
    
    def test_home_route_exists(self):
        """Test that the home route returns a valid response."""
        from app import app
        
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
    
    def test_game_route_exists(self):
        """Test that the game route returns a valid response."""
        from app import app
        
        with app.test_client() as client:
            response = client.get('/game')
            assert response.status_code == 200
