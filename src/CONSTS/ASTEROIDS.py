"""Constants related to asteroid sprites and their behavior in the game.

    This module contains configuration values for asteroid sprites, including
    their size, movement speed, behavior, etc.
"""

# Minimum velocity (in pixels per second) for asteroid movement along the X-axis to the right
ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT = 50

# Base radius (in pixels) for the smallest asteroid size
ASTEROID_MIN_RADIUS = 20

# Number of different asteroid size variations
ASTEROID_KINDS = 3

# Time interval between asteroid spawns in seconds
ASTEROID_SPAWN_RATE = 0.8  # seconds

# Maximum asteroid radius calculated as base radius multiplied by number of variations
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
