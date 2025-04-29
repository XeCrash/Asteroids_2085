import pygame
import random
from Sprites.circleshape import CircleShape
from CONSTS.COLORS import *
from CONSTS.ASTEROIDS import *

class Asteroid(CircleShape):
   def __init__(self, x, y, radius):
      """Initialize an asteroid object.
      
      Args:
          x: float - Initial x-coordinate position
          y: float - Initial y-coordinate position
          radius: float - Radius of the asteroid
          
      Returns:
          None
      """
      super().__init__(x, y, radius)
      
   def draw(self, screen):
      """Render the asteroid on the screen.
      
      Args:
          screen: pygame.Surface - The surface to draw the asteroid on
          
      Returns:
          None
      """
      pygame.draw.circle(screen, COLOR_RED, [self.position.x, self.position.y], self.radius, 2)
   
   def update(self, dt):
      """Update the asteroid's position based on its velocity.
      
      Args:
          dt: float - Delta time since last update
          
      Returns:
          None
      """
      self.position += (self.velocity * dt)
      
   def split(self, dt):
      """Split the asteroid into smaller asteroids when hit.
      
      Creates two smaller asteroids with diverging trajectories if the current
      asteroid is large enough. Removes the current asteroid.
      
      Args:
          dt: float - Delta time since last update
          
      Returns:
          None
      """
      self.kill()
      
      small_asteroid = ASTEROID_MIN_RADIUS
      
      if self.radius <= small_asteroid:
         return #do nothing 
      else:
         #  split off into two new asteroids -20 radius from the current size of the killed asteroid
         rand_angle = random.uniform(20, 50)
         new_vec2_right = self.velocity.rotate(rand_angle)
         new_vec2_left = self.velocity.rotate(-rand_angle)
         new_radius = self.radius - ASTEROID_MIN_RADIUS
         new_asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
         new_asteroid_one.velocity = (new_vec2_right * 1.2)
         new_asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
         new_asteroid_two.velocity = (new_vec2_left * 1.2)
      