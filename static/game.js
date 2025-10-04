/**
 * Nokia Snake Game - Frontend JavaScript
 * Handles game rendering, user input, and API communication
 */

class SnakeGameUI {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = 20;
        this.tileCount = this.canvas.width / this.gridSize;
        
        this.gameState = null;
        this.gameLoop = null;
        this.gameSpeed = 200; // Nokia speed (milliseconds)
        this.previousScore = 0; // Track score changes for sound triggers
        
        // Initialize sound engine
        this.soundEngine = new SoundEngine();
        
        this.initializeElements();
        this.bindEvents();
        this.createNewGame();
    }
    
    initializeElements() {
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.restartBtn = document.getElementById('restartBtn');
        this.scoreDisplay = document.getElementById('currentScore');
        this.highScoreDisplay = document.getElementById('highScore');
        this.statusDisplay = document.getElementById('gameStatus');
        this.soundToggle = document.getElementById('soundToggle');
    }
    
    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startGame());
        this.pauseBtn.addEventListener('click', () => this.pauseGame());
        this.restartBtn.addEventListener('click', () => this.restartGame());
        
        // Sound toggle
        this.soundToggle.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.soundEngine.enableSound();
            } else {
                this.soundEngine.disableSound();
            }
        });
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }
    
    handleKeyPress(event) {
        if (this.gameState && this.gameState.state === 'playing') {
            let direction = null;
            
            switch(event.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    direction = 'up';
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    direction = 'down';
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    direction = 'left';
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    direction = 'right';
                    break;
            }
            
            if (direction) {
                event.preventDefault();
                this.sendDirectionChange(direction);
            }
        }
    }
    
    async createNewGame() {
        try {
            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            this.gameState = await response.json();
            this.previousScore = 0; // Reset score tracking for sound
            this.statusDisplay.classList.remove('game-over'); // Clear game over state
            this.updateDisplay();
            this.render();
            this.statusDisplay.textContent = 'Press Start to begin';
        } catch (error) {
            console.error('Error creating new game:', error);
            this.statusDisplay.textContent = 'Error creating game';
        }
    }
    
    async startGame() {
        try {
            const response = await fetch('/api/game/start', {
                method: 'POST',
            });
            
            const result = await response.json();
            if (result.success) {
                this.gameState.state = result.state;
                this.statusDisplay.textContent = 'Game running!';
                this.soundEngine.playGameStartSound();
                this.startGameLoop();
            }
        } catch (error) {
            console.error('Error starting game:', error);
        }
    }
    
    pauseGame() {
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
            this.gameLoop = null;
            this.statusDisplay.textContent = 'Game paused';
        }
    }
    
    restartGame() {
        this.pauseGame();
        this.createNewGame();
    }
    
    async sendDirectionChange(direction) {
        try {
            await fetch('/api/game/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ direction: direction })
            });
        } catch (error) {
            console.error('Error sending direction change:', error);
        }
    }
    
    startGameLoop() {
        this.gameLoop = setInterval(async () => {
            await this.updateGame();
        }, this.gameSpeed);
    }
    
    async updateGame() {
        try {
            const response = await fetch('/api/game/update', {
                method: 'POST',
            });
            
            this.gameState = await response.json();
            
            // Check for food eaten (score increase)
            if (this.gameState.score > this.previousScore) {
                this.soundEngine.playFoodEatenSound();
                this.previousScore = this.gameState.score;
            }
            this.updateDisplay();
            this.render();
            
            if (this.gameState.state === 'game_over') {
                this.pauseGame();
                this.soundEngine.playGameOverSound();
                this.statusDisplay.textContent = 'Game Over! Score: ' + this.gameState.score;
                this.statusDisplay.classList.add('game-over');
                
                // Update high score
                const currentHigh = parseInt(this.highScoreDisplay.textContent) || 0;
                if (this.gameState.score > currentHigh) {
                    this.highScoreDisplay.textContent = this.gameState.score;
                    localStorage.setItem('snakeHighScore', this.gameState.score);
                }
                
                // Reset score tracking for next game
                this.previousScore = 0;
            }
        } catch (error) {
            console.error('Error updating game:', error);
        }
    }
    
    updateDisplay() {
        if (this.gameState) {
            this.scoreDisplay.textContent = this.gameState.score;
        }
        
        // Load high score from localStorage
        const savedHighScore = localStorage.getItem('snakeHighScore') || 0;
        this.highScoreDisplay.textContent = savedHighScore;
    }
    
    render() {
        if (!this.gameState) return;
        
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw snake
        this.ctx.fillStyle = '#0f0';
        this.gameState.snake.forEach(segment => {
            this.ctx.fillRect(
                segment[0] * this.gridSize,
                segment[1] * this.gridSize,
                this.gridSize - 2,
                this.gridSize - 2
            );
        });
        
        // Draw food
        this.ctx.fillStyle = '#ff0';
        this.ctx.fillRect(
            this.gameState.food[0] * this.gridSize,
            this.gameState.food[1] * this.gridSize,
            this.gridSize - 2,
            this.gridSize - 2
        );
        
        // Draw grid lines (Nokia style)
        this.ctx.strokeStyle = '#333';
        this.ctx.lineWidth = 1;
        
        for (let i = 0; i <= this.tileCount; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.gridSize, 0);
            this.ctx.lineTo(i * this.gridSize, this.canvas.height);
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.gridSize);
            this.ctx.lineTo(this.canvas.width, i * this.gridSize);
            this.ctx.stroke();
        }
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SnakeGameUI();
});
