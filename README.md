# Airplane Game

A 2D airplane game built with Python and Pygame. Control an airplane to avoid obstacles, collect power-ups, fight bosses, and achieve high scores!

## Features
- Multiple airplane types with different characteristics
- Boss battles with unique attack patterns
- Shooting mechanics
- Smooth airplane controls
- Obstacle avoidance gameplay
- Health system
- Multiple types of power-ups:
  - Health (Green): Restores 20 health points
  - Invincibility (Yellow): Makes you invincible for 3 seconds
  - Speed Boost (Purple): Increases speed for 5 seconds
- Level system with increasing difficulty
- High score tracking
- Sound effects and background music
- Visual effects:
  - Particle effects for collisions and power-ups
  - Starry background
  - Level-up animations
- Game over screen with restart option

## Airplane Types
1. Default (Blue)
   - Balanced speed and health
   - Speed: 5
   - Health: 100

2. Fast (Green)
   - High speed, lower health
   - Speed: 7
   - Health: 80

3. Tank (Red)
   - High health, lower speed
   - Speed: 3
   - Health: 150

## Boss Battles
- Boss appears every 5000 points
- Large orange enemy with multiple attack patterns
- Shoots bullets in 8 directions
- Moves up and down while approaching
- Defeating a boss:
  - Awards 1000 bonus points
  - Requires strategic shooting and dodging
  - Boss health increases with level

## Requirements
- Python 3.7 or higher
- Pygame
- Numpy

## Installation
1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Generate sound effects:
```bash
python generate_sounds.py
```

## How to Play
1. Run the game:
```bash
python airplane_game.py
```

2. Controls:
- Arrow keys: Move the airplane
- Space: Shoot
- 1: Switch to Default airplane
- 2: Switch to Fast airplane
- 3: Switch to Tank airplane
- R: Restart game after game over

3. Game Objective:
- Avoid obstacles and boss attacks
- Shoot and defeat the boss
- Collect power-ups to gain advantages
- Your score increases as you survive longer
- Game ends when your health reaches zero
- Try to beat your high score!

## Game Mechanics
- Each obstacle hit reduces health by 20 points
- Boss collision reduces health by 40 points
- Boss bullet hit reduces health by 10 points
- Health power-ups restore 20 health points
- Maximum health is 100 points
- High scores are saved between game sessions
- Level increases every 1000 points
- Each level:
  - Increases obstacle speed
  - Increases obstacle spawn rate
  - Makes obstacles more durable
  - Increases boss health

## Power-ups
1. Health (Green)
   - Restores 20 health points
   - Maximum health is 100

2. Invincibility (Yellow)
   - Makes you invincible for 3 seconds
   - No health loss during this time
   - Visual indicator shows when active

3. Speed Boost (Purple)
   - Increases airplane speed for 5 seconds
   - Helps dodge obstacles more easily
   - Automatically resets after duration
