import sys
import pygame
from math import pi
from datetime import datetime
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from constants import COLOR_BLACK
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from constants import ASTEROID_MIN_RADIUS, ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT

def main():
   # Add file logging setup at the start of main()
   log_file = open("GameEvents.logs", "w")
   current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   print(f"[{current_time}] Starting Asteroids!")
   print(f"[{current_time}] Screen width: {SCREEN_WIDTH}")
   print(f"[{current_time}] Screen height: {SCREEN_HEIGHT}")
   print() # Newline
   
   # Setting up initalization for the game and game window
   pygame.init()
   
   updatable_group = pygame.sprite.Group()
   drawable_group = pygame.sprite.Group()
   asteroids_group = pygame.sprite.Group()
   shot_group = pygame.sprite.Group()
   Player.containers = (updatable_group, drawable_group)
   Shot.containers = (updatable_group, drawable_group, shot_group)
   Asteroid.containers = (asteroids_group, updatable_group, drawable_group)
   AsteroidField.containers = (updatable_group) # updates POS only and its also not an asteroid itself so we only put in updatable group
   
   player_obj = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # set player sprite cords(x, y) to middle of screen
   astroid_obj = Asteroid(-100, 100, ASTEROID_MIN_RADIUS) # initalize a single Asteroid spawn
   astroid_obj.velocity = pygame.Vector2(ASTEROID_X_AXIS_MIN_VELOCITY_RIGHT, 0) # move [50] units to the right on X, [0] units on Y
   AsteroidField() # initalize the AsteroidField so it can begin spawning Asteroids
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
   clock = pygame.time.Clock()
   
   pygame.display.set_caption("Asteroids! | Programmed By (Avery R.)")
   
   counter = 0
   done = False
   dt = 0
   
   for thing in updatable_group:
            print(f"Updatable Group: {thing}")
   print() # Newline
   for thing in drawable_group:
            print(f"Drawable Group: {thing}")
   print() # Newline      
   for thing in asteroids_group:
            print(f"Asteroid Group: {thing}")
   print() # Newline
   
   # ♾️ While - The Game Loop
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            done = True
         else:
            if len(sys.argv) > 1 and sys.argv[1] == "--LOG-EVENTS":
               print(f"Unhandeled Event: {event}", file=log_file)
               log_file.flush()  # Ensure events are written immediately to log_file
            
      screen.fill(COLOR_BLACK) # Fill background of game window with color black
      for sprites in drawable_group: # We have to iterate through the group because we are using a custom draw function not default with pygame
         sprites.draw(screen) # Draws Player & Asteroid Sprite
      updatable_group.update(dt) # Updates the rotation & movement of Player, Asteroid, & AsteroidField
      
      # Player collison with asteroids detection
      for asteroid in asteroids_group:
         if player_obj.colliding_with(asteroid):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Game Over!")
            print(f"[{current_time}] Handeled Event: <CustomEvent(001-CollisionDetected ['event_desc': 'Player Collision With Asteroid Detected!'])>", file=log_file)
            log_file.close()
            sys.exit(0)
            
         # Check collisions between shots and this asteroid
         for shot in shot_group:
            if shot.colliding_with(asteroid):
               current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               print(f"[{current_time}] Handeled Event: <CustomEvent(002-CollisionDetected ['event_desc': 'Player Fired Bullet Collided With An Asteroid Enemy!'])>", file=log_file)
               shot.kill()
               asteroid.split(dt)
               break  # Break since this asteroid is now destroyed

      # If game exit event is triggered.
      if done == True:
         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         print(f"[{current_time}] User exited the game!", file=log_file)
         log_file.close()
         return
      
      pygame.display.flip() # Refreshes the screen | flip to next frame | Renders Screen which is the Game Loop's State

      # pause game for 1/60th of a second, we get the delta return time of .tick() then divide that by 1000 to get
      # seconds from the returning milliseconds value
      dt = clock.tick(SCREEN_FPS) / 1000 # 60/FPS
      if len(sys.argv) > 1 and sys.argv[1] == "--DT-PRINT":
         print(dt)
      
   # ♾️ While - The Game Loop

if __name__ == "__main__":
   main()