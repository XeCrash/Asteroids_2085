import sys
import pygame
import logging
from CONSTS.KEYS import K_HELD, KEY_ESCAPE
from MyUtils.helpermethods import MyHelpers as util
from HUDUtils.hud import HUD
from MenuUtils.menu import Menu
from Sprites.player import Player
from Sprites.asteroid import Asteroid
from Sprites.asteroidfield import AsteroidField
from Sprites.shot import Shot
from CONSTS.COLORS import COLOR_BLACK
from CONSTS.SCREEN import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_FLAGS,
    SCREEN_CAPTION,
    SCREEN_FPS,
)
from CONSTS.ASTEROIDS import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT,
)


# logging.disable()
logging.basicConfig(
    filename="internal_debug.logs",
    level=logging.INFO,
    format="[%(asctime)s] <-> [%(levelname)s] <-> ['%(message)s']",
)


def game_loop(  # TODO: cut down on game_loop complexity (cur: 27) aiming for a max of 15.
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    menu: Menu,
    game_state: str,
    logs_to_print: str,
    log_spam_once=True,
    clear_internal_debug_on_run=False,
):
    """Main game loop. Handling Menu's, gameplay, & state management.
    Args:
        screen: pygame.Surface - The main display surface
        clock: pygame.time.Clock - Game clock for controlling frame rate
        menu: Menu - The game menu instance
        game_state: str - Current state of the game ('menu' or 'game')
        logs_to_print: str - The type of logs to print to the console ('none', 'all', 'debug', 'events')
        log_spam_once: bool - Whether to log certain loop bound info to the console once or not.
        clear_internal_debug_on_run: bool - When True, internal_debug.logs file is cleared just like the other logging file.  # noqa: E501

    Returns:
        None
    """
    # TODO: remove this when done with development and testing, Debug purposes.

    if logs_to_print.lower() in ["all", "errors"]:
        content = util.read_file_with_retry(
            ["./internal_debug.logs", "./src/internal_debug.logs"]
        )
        if content:
            util.print_error_logs(content)
        else:
            msg = (
                "Failed to find internal_debug.logs."
                if logs_to_print.lower() == "all"
                else "Failed to read any of the specified files."
            )
            logging.error(msg) if logs_to_print.lower() == "all" else print(msg)  # noqa: E501

    if logs_to_print.lower() in ["all", "events"]:
        content = util.read_file_with_retry(
            ["./GameEvent.logs", "./src/GameEvent.logs"]
        )
        if content:
            util.print_event_logs(content)
        else:
            msg = (
                "Failed to find GameEvent.logs"
                if logs_to_print.lower() == "all"
                else "Failed to read any of the specified files."
            )
            logging.error(msg) if logs_to_print.lower() == "all" else print(msg)  # noqa: E501

    # util.print_log_contents(logs_to_print)

    # Add file logging setup
    log_file = open("GameEvent.logs", "w")
    print("[Current Session]")
    print(f"[{util.get_dt_now()}] Starting Asteroids!")

    # logging
    logging.info("game_loop() method started.")
    # initialize delta time variable
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
        if log_spam_once is True:
            logging.info("Entering ♾️ while game loop...")

        if game_state == "menu":
            if log_spam_once is True:
                logging.info("Entering menu loop...")
            screen.fill(COLOR_BLACK)
            menu.draw(screen)
            action = menu.handle_input()

            if action == "start game" and menu.update_transition():
                game_state = "game"
                # Set container groups for game objects before initialization
                Player.containers = updatable_group, drawable_group
                Shot.containers = updatable_group, drawable_group, shot_group
                Asteroid.containers = asteroids_group, updatable_group, drawable_group  # noqa: E501
                AsteroidField.containers = updatable_group
                # Initialize game objects when transitioning to game state
                player_obj = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                asteroid_field = AsteroidField()  # noqa: F841
                # TODO: add a way to save player state and restore it when returning from main menu  # noqa: E501
                # TODO: add a way to save asteroidfield state and restore it when returning from main menu  # noqa: E501
                astroid_obj = Asteroid(-100, 100, ASTEROID_MIN_RADIUS)
                astroid_obj.velocity = pygame.Vector2(
                    ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT, 0
                )

            elif action == "controls":
                # Add controls screen implementation here
                pass
            elif action == "credits":
                # Add credits screen implementation here
                pass
            elif action == "exit" or action == "quit":
                print(
                    f"[{util.get_dt_now()}] User exited the game via the menu!",  # noqa: E501
                    file=log_file,
                )
                log_file.close()
                print()
                if clear_internal_debug_on_run is True:
                    util.clear_file_rplus("internal_debug.logs")
                return

        elif game_state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    print(
                        f"[{util.get_dt_now()}] User exited the game via the window X!",  # noqa: E501
                        file=log_file,
                    )
                    log_file.close()
                    return
                elif event.type == K_HELD and event.key == KEY_ESCAPE:
                    game_state = "menu"

                    # Reset title fade alpha to restart fade in effect
                    menu.title_fade_alpha = 0
                    # menu.update_transition()
                    menu.transitioning = False
                    menu.transition_alpha = 255
                    menu.update_transition()
                    menu.handle_music_state()  # Switch back to menu music

                    # Clear all sprite groups
                    updatable_group.empty()
                    drawable_group.empty()
                    asteroids_group.empty()
                    shot_group.empty()
                    # Reset player object fields
                    # player_obj.reset()
                else:
                    if len(sys.argv) > 1 and sys.argv[1] == "--LOG-EVENTS":
                        print(f"Unhandeled Event: {event}", file=log_file)
                        log_file.flush()

            # Update and draw game objects
            screen.blit(menu.get_game_background(), (0, 0))

            # Draw all sprites
            for sprites in drawable_group:
                sprites.draw(screen)
            updatable_group.update(clock.get_time() / 1000)

            # Draw HUD elements
            if player_obj is not None:
                # Draw HUD elements only when the player is alive
                HUD.draw(screen, player_obj.kill_count)

            # Collision detection code...
            for asteroid in asteroids_group:
                if player_obj.colliding_with(asteroid):
                    print(f"[{util.get_dt_now()}] Game Over!")
                    print(
                        f"[{util.get_dt_now()}] <CustomEvent(001-CollisionDetected ['event_desc': 'Player Collision With Asteroid Detected!'])>",  # noqa: E501
                        file=log_file,
                    )

                    # Show game over background briefly before returning to menu  # noqa: E501
                    screen.blit(menu.get_game_over_background(), (0, 0))
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Wait 2 seconds to show game over screen  # noqa: E501

                    # game state switching back to menu
                    game_state = "menu"

                    # transition effects
                    menu.transitioning = False
                    menu.transition_alpha = 255
                    menu.title_fade_alpha = 0  # Reset the title fade alpha to start the fade in effect over again  # noqa: E501
                    menu.update_transition()
                    menu.handle_music_state()
                    # Clear all sprite groups
                    updatable_group.empty()
                    drawable_group.empty()
                    asteroids_group.empty()
                    shot_group.empty()

                    # Reset player object fields
                    # player_obj.reset()

                    # break out of the loop
                    break

            # Check collisions between shots and all asteroids
            for shot in shot_group:
                for asteroid in asteroids_group:
                    if shot.colliding_with(asteroid):
                        player_obj.kill_count += 1
                        print(
                            f"[{util.get_dt_now()}] <CustomEvent(002-BulletCollisionDetected ['player_obj.kill_count': '{player_obj.kill_count}', event_desc': 'Player killed an enemy!'])>",  # noqa: E501
                            file=log_file,
                        )
                        shot.kill()
                        asteroid.split()
                        # Draw HUD elements
                        HUD.draw(screen, player_obj.kill_count)
                        break  # Break inner loop since this shot hit an asteroid

        # Update display & control frame rate
        pygame.display.flip()
        dt = clock.tick(SCREEN_FPS) / 1000
        if log_spam_once is True:
            logging.info(f"Screen updated! Delta Time: {dt}")
        log_spam_once = False  # Set to False to prevent logging this information repeatedly in console  # noqa: E501


def main():
    """Initialize and start the Asteroids game.

    Sets up the pygame environment, creates the game window, and starts the main game loop.  # noqa: E501

    Returns:
        None
    """
    logging.info("main() method started.")
    pygame.init()
    HUD.init_font()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_FLAGS)
    clock = pygame.time.Clock()
    pygame.display.set_caption(SCREEN_CAPTION)

    # Load program icon and set it
    try:
        logging.info("Loading 'Icon.png'...")
        icon = pygame.image.load("./Assets/Images/Icon.png")
    except FileNotFoundError:
        logging.error(
            "Failed to find 'Icon.png' with path './Assets/Images/Icon.png', retrying icon loading with path './src/Assets/Images/Icon.png'!"  # noqa: E501
        )
        retry_icon = pygame.image.load("./src/Assets/Images/Icon.png")

        if retry_icon is None:
            logging.critical("Failed to load 'Icon.png'!")
            sys.exit(1)
        else:
            logging.info(
                "Loaded 'Icon.png' on the 2nd path outside of ./src directory!"
            )
            icon = retry_icon

    pygame.display.set_icon(icon)
    logging.info("Icon loaded on display surface!")

    # Initialize menu as our starting game state so we see the menu screen when loaded in for the first time  # noqa: E501
    logging.info("Game state is being setting...")
    menu = Menu(screen)
    game_state = "menu"
    logging.info("Game state set to 'menu'!")

    logging.info("main() method finished!")
    game_loop(
        screen,
        clock,
        menu,
        game_state,
        logs_to_print="all",
        clear_internal_debug_on_run=True,
    )


if __name__ == "__main__":
    """Entry point for the game.

    Initializes the game and starts the main loop.
    """
    main()
