"""Constants related to the game window of Asteroids 2085.
    
This module contains configuration for the game window & related settings, including
dimensions, frame rate, and display flags.
"""

import pygame
# Window width in pixels (16:9 aspect ratio)
SCREEN_WIDTH = 1280

# Window height in pixels (16:9 aspect ratio)
SCREEN_HEIGHT = 720

# Target frame rate for the game
SCREEN_FPS = 165

# Pygame display flags for window behavior
# SCALED: Maintains aspect ratio when resizing
# RESIZABLE: Allows window resizing
SCREEN_FLAGS = pygame.SCALED | pygame.RESIZABLE

# Window title bar text
SCREEN_CAPTION = "Asteroids! | Programmed By (Avery R.)"