"""Constants related to the main menu of the Asteroids 2085. 

This module contains configuration values for the menu, including options,
text, and animation settings.
"""
# Imports
from CONSTS.COLORS import *

# List of available menu options shown to the player
MENU_STATES_LIST = ['Start Game', 'Controls', 'Exit', 'Credits']

# Title text displayed at the top of the main menu
MENU_TITLE_TEXT = 'ASTEROIDS 2085'

# Background music volume level (0.0 to 1.0)
MENU_MUSIC_VOLUME = 0.1

# Speed of the title text fade animation in units per second
MENU_TITLE_FADE_SPEED = 1.5

# Font size for the menu title text in pixels
MENU_TITLE_FONT_SIZE = 100

# Font size for menu option text in pixels
MENU_OPTION_FONT_SIZE = 50

# Default color for unselected menu options
MENU_OPTION_COLOR = COLOR_RED

# Highlight color for the currently selected menu option
MENU_OPTION_SELECTED_COLOR = COLOR_YELLOW

# Color of the selection arrow indicator
MENU_OPTION_ARROW_COLOR = COLOR_WHITE

# Vertical spacing between menu options in pixels (Critical for layout)
MENU_OPTION_SPACING = 50 # DONT CHANGE THIS unless you know what you are doing

# Size of the selection arrow indicator in pixels
MENU_OPTION_ARROW_SIZE = 20 # TODO: NOT IMPLEMENTED YET (NO REFERENCES... YET)

# Horizontal spacing between arrow and menu text in pixels
MENU_OPTION_ARROW_SPACING = 30 # TODO: NOT IMPLEMENTED YET (NO REFERENCES... YET)

# Horizontal offset of the arrow from menu edge in pixels
MENU_OPTION_ARROW_OFFSET = 50 # TODO: NOT IMPLEMENTED YET (NO REFERENCES... YET)

# Speed of menu transition animations in alpha units per frame
MENU_TRANSITION_SPEED = 2  # Alpha change per frame

# Duration of menu transition animations in seconds
MENU_TRANSITION_DURATION = 0.5  # seconds