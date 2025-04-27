import pygame
import os
import math
from CONSTS.SCREEN import *
from CONSTS.MENUCONFIG import *

class Menu:
    def __init__(self, screen):
        """Initialize the menu system with display settings and audio.
        
        Args:
            screen: pygame.Surface - The main game display surface
            
        Returns:
            None
        """
        self.screen = screen
        self.font_large = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        self.font_small = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)
        self.selected_option = 0
        self.options = MENU_STATES_LIST
        self.transition_alpha = 255  # For fade effect
        self.transitioning = False
        self.title_animation_time = 0
        self.title_fade_alpha = 0  # For title fade-in effect
        
        # Initialize music
        pygame.mixer.init()
        self.menu_music = None
        self.game_music = None
        
        # Load music if files exist
        menu_music_path = os.path.join(os.path.dirname(__file__), '../', 'Assets', 'Audio', 'menu_music.mp3')
        game_music_path = os.path.join(os.path.dirname(__file__), '../', 'Assets', 'Audio', 'game_music.mp3')
        
        if os.path.exists(menu_music_path):
            self.menu_music = pygame.mixer.Sound(menu_music_path)
            self.menu_music.set_volume(MENU_MUSIC_VOLUME)
            self.menu_music.play(-1)  # Loop indefinitely
        else:
            print(f"Menu music file not found at {menu_music_path}")
        
        if os.path.exists(game_music_path):
            self.game_music = pygame.mixer.Sound(game_music_path)
        else:
            print(f"Game music file not found at {game_music_path}")

    def draw(self, screen):
        """Renders the menu interface with animated title and options.
        
        Args:
            screen: pygame.Surface - The surface to draw the menu on
            
        Returns:
            None
        """
        self.screen.fill(COLOR_BLACK)
        
        # Update title animation time
        self.title_animation_time += 0.05
        if self.title_animation_time > 2 * math.pi:
            self.title_animation_time -= 2 * math.pi
        
        # Update title fade-in effect
        if self.title_fade_alpha < 255:
            self.title_fade_alpha += MENU_TITLE_FADE_SPEED  # Gradually increase opacity
            
        
        # Draw animated title with unique design
        title_text = MENU_TITLE_TEXT
        title_center_x = SCREEN_WIDTH/2
        title_center_y = SCREEN_HEIGHT/4
        
        # Create a unique, animated title
        # First calculate the total width more accurately
        total_width = 0
        char_surfaces = []
        char_widths = []
        char_color = [255, 255, 0]  # Initial color
        
        for char in title_text:
            char_surface = self.font_large.render(char, True, (255, 255, 255))  # Temporary for width calculation
            char_width = char_surface.get_width()
            char_widths.append(char_width)
            total_width += char_width
        
        # Add a small gap between characters (10% of average character width)
        char_gap = sum(char_widths) / len(char_widths) * 0.1
        total_width += char_gap * (len(title_text) - 1)
        
        # Now render and position each character
        current_x = title_center_x - total_width/2
        
        for i, char in enumerate(title_text):
            # Calculate position with wave effect
            offset_y = math.sin(self.title_animation_time + i * 0.3) * 10
            
            # Color gradient
            char_color_r, char_color_g, char_color_b = (255, 255 - i * 15, i * 25)
            char_color = (char_color_r, char_color_g, char_color_b)
            # Render each character separately
            if char_color_b <= 255: 
                # While blue is not maxed out
                #print(char_color) # TODO: Remove (Debugging)
                char_surface = self.font_large.render(char, True, char_color)
            else: 
                # Once blue is maxed out
                char_surface = self.font_large.render(char, True, (char_color_r, char_color_g, 255))  # White for the last few characters
            
            # Position each character
            pos_x = current_x
            pos_y = title_center_y + offset_y
            
            # Add shadow effect
            shadow = self.font_large.render(char, True, (50, 50, 50))
            
            # Apply fade-in effect to both character and shadow
            char_surface.set_alpha(self.title_fade_alpha)
            shadow.set_alpha(self.title_fade_alpha)
            
            # Draw the shadow and character
            screen.blit(shadow, (pos_x + 3, pos_y + 3))
            screen.blit(char_surface, (pos_x, pos_y))
            
            # Move to the next character position
            current_x += char_widths[i] + char_gap

        # Draw menu options
        for i, option in enumerate(self.options):
            # Use blue color for menu text, but keep selection indicators white
            if i == self.selected_option:
                # Render the option text in blue
                option_text = self.font_small.render(option, True, MENU_OPTION_SELECTED_COLOR) # TODO: add CONST MENU_OPTION_COLOR
                
                # Calculate positions for the text
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i * MENU_OPTION_SPACING))
                
                # Render the left and right arrows separately in white
                left_arrow = self.font_small.render('>', True, MENU_OPTION_ARROW_COLOR)
                right_arrow = self.font_small.render('<', True, MENU_OPTION_ARROW_COLOR)
                
                # Position arrows with proper spacing based on text width
                left_arrow_pos = (option_rect.left - left_arrow.get_width() - 5, option_rect.top)
                right_arrow_pos = (option_rect.right + 5, option_rect.top)
                
                # Draw text and arrows separately
                screen.blit(option_text, option_rect)
                screen.blit(left_arrow, left_arrow_pos)
                screen.blit(right_arrow, right_arrow_pos)
            else:
                # Non-selected options are just red
                text = self.font_small.render(option, True, MENU_OPTION_COLOR)
                rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i * 50))
                screen.blit(text, rect)

        # Draw transition overlay if needed
        if self.transitioning:
            transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            transition_surface.fill(COLOR_BLACK)
            transition_surface.set_alpha(self.transition_alpha)
            screen.blit(transition_surface, (0, 0))

    def handle_input(self):
        """Processes keyboard input for menu navigation and selection.
        
        Returns:
            str: Selected menu option or None if no selection made
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.transitioning = True
                    return self.options[self.selected_option].lower()
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] and keys[pygame.K_w]:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                if keys[pygame.K_LSHIFT] and keys[pygame.K_s]:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                if keys[pygame.K_LSHIFT] and keys[pygame.K_e]:
                    self.transitioning = True
                    return self.options[self.selected_option].lower()
        return None

    def update_transition(self):
        """Updates the transition effect between menu and game states.
        
        Returns:
            bool: True if transition is complete, False otherwise
        """
        if self.transitioning:
            self.transition_alpha += MENU_TRANSITION_SPEED
            if self.transition_alpha >= 255:
                # Stop menu music and start game music when transitioning to game
                if self.menu_music:
                    self.menu_music.stop()
                if self.game_music:
                    self.game_music.play(-1)
                return True
        return False
        
    def return_to_menu(self):
        """Handles the transition from game state back to menu state.
        
        Returns:
            None
        """
        # Stop game music and restart menu music
        if self.game_music:
            self.game_music.stop()
        if self.menu_music:
            self.menu_music.play(-1)