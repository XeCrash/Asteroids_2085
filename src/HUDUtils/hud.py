import pygame
from CONSTS.COLORS import COLOR_YELLOW, COLOR_PURPLE
from CONSTS.FONTS import FONT_DAYDREAM, FONT_DAYDREAM_PATH2


class HUD:
    # Class variable for the font
    font_default = None
    kills_label_surface = None
    last_kill_count = None
    kill_num_surface = None

    @staticmethod
    def init_font():
        """Initialize the font. Call this after pygame.init()"""
        try:
            HUD.font_default = pygame.font.Font(
                FONT_DAYDREAM, 16
            )  # Default Pygame font, size 36
        except pygame.error:
            print("Failed to load font. Trying 2nd path too game font.")
            # If the font fails to load, use another path to load the font
            HUD.font_default = pygame.font.Font(
                FONT_DAYDREAM_PATH2, 16
            )
        # Pre-render static label and init counters
        HUD.kills_label_surface = HUD.font_default.render("Kills:", True, COLOR_YELLOW)
        HUD.kill_num_surface = HUD.font_default.render("0", True, COLOR_PURPLE)
        HUD.last_kill_count = 0

    @staticmethod
    def draw(screen, kill_count: int):
        """Draw the HUD elements on the screen.

        Args:
            screen: pygame.Surface - The main display surface
            kill_count: int - The current number of kills by the player
        """
        # Use cached label; update number surface only when needed
        kill_text = HUD.kills_label_surface
        kill_txt_rect = kill_text.get_rect()
        if kill_count != HUD.last_kill_count or HUD.kill_num_surface is None:
            HUD.kill_num_surface = HUD.font_default.render(f"{kill_count}", True, COLOR_PURPLE)
            HUD.last_kill_count = kill_count
        kill_num = HUD.kill_num_surface
        kill_num_rect = kill_num.get_rect()

        # Position the text in the top-left corner with some padding
        kill_txt_rect.topleft = (10, 10)
        # Position the text to the right of the kill count text
        kill_num_rect.topleft = (
            kill_txt_rect.topright[0] + 10,
            kill_txt_rect.topright[1],
        )

        # Draw the text on the screen
        screen.blit(kill_text, kill_txt_rect)
        screen.blit(kill_num, kill_num_rect)
