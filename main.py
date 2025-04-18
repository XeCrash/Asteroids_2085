import sys
import pygame
from player import Player
from constants import COLOR_BLACK
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE, ASTEROID_MAX_RADIUS

def main():
   print("Starting Asteroids!")
   print(f"Screen width: {SCREEN_WIDTH}")
   print(f"Screen height: {SCREEN_HEIGHT}")
    
    #setting up initalization for the game and game window
   pygame.init()
   updatable = pygame.sprite.Group()
   drawable = pygame.sprite.Group()
   Player.containers = (updatable, drawable)
   player_sprite = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) #set player sprite cords(x, y) to middle of screen
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()
   dt = 0
   
   for thing in updatable:
      print(f"Thing: {thing}")
   
   # ♾️ While - The Game Loop
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
            
      screen.fill(COLOR_BLACK)
      for p1_sprite in drawable:
         p1_sprite.draw(screen)
      updatable.update(dt) #Updates the rotation of player sprite
      pygame.display.flip() #refreshes the screen | flip to next frame | Renders Screen which is the Game Loop's State

      # pause game for 1/60th of a second and get the delta return time of .tick() / 1000 to get
      # seconds from the returning milliseconds value
      dt = clock.tick(SCREEN_FPS) / 1000 # 60/FPS
      if len(sys.argv) > 1 and sys.argv[1] == "--DT-PRINT":
         print(dt)
      
   # ♾️ While - The Game Loop

if __name__ == "__main__":
   main()