import sys
import pygame
from math import pi
from datetime import datetime
import logging
from MenuUtils.menu import Menu
from Sprites.player import Player
from Sprites.asteroid import Asteroid
from Sprites.asteroidfield import AsteroidField
from Sprites.shot import Shot
from CONSTS.COLORS import COLOR_BLACK
from CONSTS.SCREEN import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS, SCREEN_CAPTION, SCREEN_FLAGS
from CONSTS.ASTEROIDS import ASTEROID_MIN_RADIUS, ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT

#logging.disable()
logging.basicConfig(filename='internal_debug.logs', level=logging.INFO, format='[%(asctime)s] <-> [%(levelname)s] <-> [\'%(message)s\']')

def game_loop(screen, clock, menu, game_state, log_file, log_once = True):
    """Main game loop. Handling menu navigation, gameplay, and state transitions.
    
    Args:
        screen: pygame.Surface - The main display surface
        clock: pygame.time.Clock - Game clock for controlling frame rate
        menu: Menu - The game menu instance
        game_state: str - Current state of the game ('menu' or 'game')
        log_file: file - File object for logging game events
        
    Returns:
        None
    """
    logging.info("game_loop() method started.")
    dt = 0
    # Initialize sprite groups
    logging.info("Initializing sprite groups...")
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()
    logging.info("Sprite groups initialized.")
    
    # Set container groups for game objects
    logging.info("Setting container groups for game objects...")
    Player.containers = updatable_group, drawable_group
    Shot.containers = updatable_group, drawable_group, shot_group
    Asteroid.containers = asteroids_group, updatable_group, drawable_group
    AsteroidField.containers = updatable_group
    logging.info("Container groups set.")
    
    # Initialize game objects as None
    logging.info("Initializing game objects...")
    player_obj = None
    asteroid_field = None
    logging.info("Game objects initialized.")
    
    while True:
        if log_once is True:
            logging.info("Entering ♾️ game loop...")
            
        if game_state == "menu":
            if log_once is True:
                logging.info("Entering menu loop...")
            screen.fill(COLOR_BLACK)
            menu.draw(screen)
            action = menu.handle_input()
            
            if action == "start game" and menu.update_transition():
                game_state = "game"
                # Set container groups for game objects before initialization
                Player.containers = updatable_group, drawable_group
                Shot.containers = updatable_group, drawable_group, shot_group
                Asteroid.containers = asteroids_group, updatable_group, drawable_group
                AsteroidField.containers = updatable_group
                # Initialize game objects when transitioning to game state
                player_obj = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                asteroid_field = AsteroidField()
                # TODO: add a way to save player state and restore it when returning from main menu
                # TODO: add a way to save asteroidfield state and restore it when returning from main menu
                astroid_obj = Asteroid(-100, 100, ASTEROID_MIN_RADIUS)
                astroid_obj.velocity = pygame.Vector2(ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT, 0)
                
            elif action == "controls":
                # Add controls screen implementation here
                pass
            elif action == "credits":
                # Add credits screen implementation here
                pass
            elif action == "exit" or action == "quit":
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] User exited the game via the menu!", file=log_file)
                log_file.close()
                return
                
        elif game_state == "game":
            # Your existing game loop code here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{current_time}] User exited the game via the window X!", file=log_file)
                    log_file.close()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    player_obj.kill_count = 0
                    menu.title_fade_alpha = 0 # Reset the title fade alpha to start the fade in effect over again
                    menu.transitioning = False
                    menu.transition_alpha = 255
                    menu.update_transition() 
                    menu.return_to_menu()  # Switch back to menu music
                    # Clear all sprite groups
                    updatable_group.empty()
                    drawable_group.empty()
                    asteroids_group.empty()
                    shot_group.empty()
                    # Reset game objects
                    player_obj = None
                    asteroid_field = None
                else:
                    if len(sys.argv) > 1 and sys.argv[1] == "--LOG-EVENTS":
                        print(f"Unhandeled Event: {event}", file=log_file)
                        log_file.flush()

            # Update and draw game objects
            screen.fill(COLOR_BLACK)
            for sprites in drawable_group:
                sprites.draw(screen)
            updatable_group.update(clock.get_time() / 1000)
            
            # Collision detection code...
            for asteroid in asteroids_group:
               if player_obj.colliding_with(asteroid):
                  current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                  print(f"[{current_time}] Game Over!")
                  print(f"[{current_time}] <CustomEvent(001-CollisionDetected ['event_desc': 'Player Collision With Asteroid Detected!'])>", file=log_file)
                  game_state = "menu"
                  menu.transitioning = False
                  menu.transition_alpha = 255
                  menu.return_to_menu()  # Switch back to menu music
                  # Clear all sprite groups
                  updatable_group.empty()
                  drawable_group.empty()
                  asteroids_group.empty()
                  shot_group.empty()
                  # Reset game objects
                  player_obj = None
                  asteroid_field = None
                  break
                
            # Check collisions between shots and all asteroids
            for shot in shot_group:
               for asteroid in asteroids_group:
                  if shot.colliding_with(asteroid):
                     player_obj.kill_count += 1
                     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                     print(f"[{current_time}] <CustomEvent(002-BulletCollisionDetected ['player_obj.kill_count': '{player_obj.kill_count}', event_desc': 'Player killed an enemy!'])>", file=log_file)
                     shot.kill()
                     asteroid.split(dt)
                     break  # Break inner loop since this shot hit an asteroid
        pygame.display.flip()
        dt = clock.tick(SCREEN_FPS) / 1000
        if log_once is True:
            logging.info("Screen updated!")
        log_once = False # Set to False to prevent logging this information again
        

def main():
    """Initialize and start the Asteroids game.
    
    Sets up the pygame environment, creates the game window, and starts the main game loop.
    
    Returns:
        None
    """
    logging.info("main() method started.")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_FLAGS)
    clock = pygame.time.Clock()
    pygame.display.set_caption(SCREEN_CAPTION)

    # Initialize menu
    menu = Menu(screen)
    game_state = "menu"
    
    # Add file logging setup
    log_file = open("GameEvent.logs", "w")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Starting Asteroids!")
    
    logging.info("main() method finished!")
    game_loop(screen, clock, menu, game_state, log_file)

if __name__ == "__main__":
    """Entry point for the game.

    Initializes the game and starts the main loop.
    """
    main()