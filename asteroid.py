import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
   def __init__(self, x, y, radius):
      super().__init__(x, y, radius)
      
   def draw(self, screen):
      pygame.draw.circle(screen, COLOR_RED, [self.position.x, self.position.y], self.radius, 2)
   
   def update(self, dt):
      self.position += (self.velocity * dt)
      
   def split(self, dt):
      self.kill()
      
      small_asteroid = ASTEROID_MIN_RADIUS
      medium_asteroid = ASTEROID_MIN_RADIUS * 2 
      large_asteroid = ASTEROID_MIN_RADIUS * 3
      
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
      