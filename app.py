"""
Flask web application for Nokia 1100 Snake Game.
Web interface and API for the classic snake game.
"""

from flask import Flask, render_template, jsonify, request
from game_engine import SnakeGame, Direction, GameState

# Create Flask application instance
app = Flask(__name__)

# Basic configuration
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'nokia-snake-game-secret-key'

# Global game instance (in production, this would be session-based)
game_instance = None


@app.route('/')
def home():
    """Home page route."""
    return '<h1>Nokia Snake Game</h1><p>Welcome to the classic Snake game!</p><a href="/game">Play Game</a>'


@app.route('/game')
def game():
    """Game page route."""
    return render_template('game.html')


# Game API Endpoints

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Create a new game instance."""
    global game_instance
    game_instance = SnakeGame()
    
    return jsonify({
        'snake': game_instance.snake_body,
        'food': game_instance.food_position,
        'score': game_instance.score,
        'state': game_instance.state.value
    })


@app.route('/api/game/state', methods=['GET'])
def game_state():
    """Get current game state."""
    global game_instance
    if not game_instance:
        game_instance = SnakeGame()
    
    return jsonify({
        'snake': game_instance.snake_body,
        'food': game_instance.food_position,
        'score': game_instance.score,
        'state': game_instance.state.value
    })


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start the game."""
    global game_instance
    if not game_instance:
        game_instance = SnakeGame()
    
    game_instance.start()
    
    return jsonify({
        'success': True,
        'state': game_instance.state.value
    })


@app.route('/api/game/move', methods=['POST'])
def move_snake():
    """Change snake direction."""
    global game_instance
    if not game_instance:
        return jsonify({'success': False, 'error': 'No active game'})
    
    direction_str = request.json.get('direction', '').lower()
    direction_map = {
        'up': Direction.UP,
        'down': Direction.DOWN,
        'left': Direction.LEFT,
        'right': Direction.RIGHT
    }
    
    if direction_str in direction_map:
        game_instance.change_direction(direction_map[direction_str])
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid direction'})


@app.route('/api/game/update', methods=['POST'])
def update_game():
    """Update game state (move snake one step)."""
    global game_instance
    if not game_instance:
        return jsonify({'success': False, 'error': 'No active game'})
    
    if game_instance.state == GameState.PLAYING:
        game_instance.move()
        game_instance.update()
    
    return jsonify({
        'snake': game_instance.snake_body,
        'food': game_instance.food_position,
        'score': game_instance.score,
        'state': game_instance.state.value
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
