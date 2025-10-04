/**
 * Sound Engine for Nokia Snake Game
 * Generates programmatic beeps using Web Audio API
 */

class SoundEngine {
    constructor() {
        this.audioContext = null;
        this.soundEnabled = true; // Enabled by default as requested
        this.initializeAudioContext();
    }
    
    initializeAudioContext() {
        try {
            // Create AudioContext (with vendor prefixes for compatibility)
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.warn('Web Audio API not supported:', error);
            this.soundEnabled = false;
        }
    }
    
    enableSound() {
        this.soundEnabled = true;
    }
    
    disableSound() {
        this.soundEnabled = false;
    }
    
    /**
     * Generate a programmatic beep tone
     * @param {number} frequency - Frequency in Hz
     * @param {number} duration - Duration in milliseconds
     * @param {number} volume - Volume (0.0 to 1.0)
     */
    generateBeep(frequency, duration, volume = 0.3) {
        if (!this.soundEnabled || !this.audioContext) {
            return;
        }
        
        try {
            // Resume AudioContext if it's suspended (browser autoplay policy)
            if (this.audioContext.state === 'suspended') {
                this.audioContext.resume();
            }
            
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            // Connect nodes: oscillator -> gain -> destination
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            // Configure oscillator
            oscillator.type = 'square'; // Nokia-style square wave
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            
            // Configure gain (volume envelope)
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(volume, this.audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration / 1000);
            
            // Start and stop oscillator
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration / 1000);
            
        } catch (error) {
            console.warn('Error generating beep:', error);
        }
    }
    
    /**
     * Play food eaten sound - happy high-pitched beep
     */
    playFoodEatenSound() {
        this.generateBeep(800, 150, 0.3);
    }
    
    /**
     * Play game over sound - descending tone sequence
     */
    playGameOverSound() {
        if (!this.soundEnabled || !this.audioContext) {
            return;
        }
        
        // Descending sequence: G, E, C (Nokia style)
        setTimeout(() => this.generateBeep(392, 200, 0.4), 0);   // G4
        setTimeout(() => this.generateBeep(330, 200, 0.4), 250); // E4
        setTimeout(() => this.generateBeep(262, 400, 0.4), 500); // C4
    }
    
    /**
     * Play game start sound - simple startup beep
     */
    playGameStartSound() {
        this.generateBeep(523, 200, 0.3); // C5
    }
}
