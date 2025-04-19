import sys
import pygame
from asteroidfield import AsteroidField
from asteroid import Asteroid
from player import Player
from constants import COLOR_BLACK
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE, ASTEROID_MAX_RADIUS, ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT

def main():
   print("Starting Asteroids!")
   print(f"Screen width: {SCREEN_WIDTH}")
   print(f"Screen height: {SCREEN_HEIGHT}")
    
   #setting up initalization for the game and game window
   pygame.init()
   updatable_group = pygame.sprite.Group()
   drawable_group = pygame.sprite.Group()
   asteroids_group = pygame.sprite.Group()
   Player.containers = (updatable_group, drawable_group)
   Asteroid.containers = (asteroids_group, updatable_group, drawable_group)
   AsteroidField.containers = (updatable_group)
   Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) #set player sprite cords(x, y) to middle of screen
   astroid_class = Asteroid(-100, 100, ASTEROID_MIN_RADIUS)
   astroid_class.velocity = pygame.Vector2(ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT, 0) #move 20 units to the right 0 units down
   AsteroidField()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()
   dt = 0
   
   for thing in asteroids_group:
      print(f"Thing: {thing}")
   
   # ♾️ While - The Game Loop
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
            
      screen.fill(COLOR_BLACK)
      for sprites in drawable_group:
         sprites.draw(screen)
      updatable_group.update(dt) #Updates the rotation of player sprite
      pygame.display.flip() #refreshes the screen | flip to next frame | Renders Screen which is the Game Loop's State

      # pause game for 1/60th of a second and get the delta return time of .tick() / 1000 to get
      # seconds from the returning milliseconds value
      dt = clock.tick(SCREEN_FPS) / 1000 # 60/FPS
      if len(sys.argv) > 1 and sys.argv[1] == "--DT-PRINT":
         print(dt)
      
   # ♾️ While - The Game Loop

if __name__ == "__main__":
   main()