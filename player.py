import pygame
from constants import PLAYER_RADIUS, PLAYER_POLYGON_LINE_WIDTH, PLAYER_TURN_SPEED, COLOR_WHITE
from circleshape import CircleShape


# Base class for player objects
class Player(CircleShape):
   def __init__(self, x, y):
      super().__init__(x, y, PLAYER_RADIUS)
      self.rotation = 0
      
   # in the player class
   def triangle(self):
      forward = pygame.Vector2(0, 1).rotate(self.rotation)
      right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
      a = self.position + forward * self.radius
      b = self.position - forward * self.radius - right
      c = self.position - forward * self.radius + right
      return [a, b, c]
      
      # overides func draw(self, screen) in CircleShape class
   def draw(self, screen):
      pygame.draw.polygon(screen, COLOR_WHITE, self.triangle(), PLAYER_POLYGON_LINE_WIDTH)
   
   def rotate(self, dt):
      self.rotation += (PLAYER_TURN_SPEED * dt)

   def update(self, dt):
      keys = pygame.key.get_pressed()

      if keys[pygame.K_w]: #Forward
         #self.rotate(dt)
         pass
            
      if keys[pygame.K_a]: #Left
         self.rotate(-dt) 
 
      if keys[pygame.K_s]: #Backwards
         #self.rotate(dt)
         pass
         
      if keys[pygame.K_d]: #right
         self.rotate(dt)
         