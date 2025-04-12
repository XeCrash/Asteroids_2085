import pygame
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE, ASTEROID_MAX_RADIUS

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    #setting up initalization for the game and game window
    pygame.init()
    player_sprite = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    
    # ♾️ While - Our Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")
        player_sprite.draw(screen)
        pygame.display.flip()

        # pause game for 1/60th of a second and get the delta return time of .tick() / 1000 to get
        # seconds from the returning milliseconds value
        dt = clock.tick(SCREEN_FPS) / 1000
        print(dt) 

if __name__ == "__main__":
    main()