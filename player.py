import pygame
from constants import PLAYER_RADIUS, PLAYER_POLYGON_LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, COLOR_WHITE
from circleshape import CircleShape


# Base class for player objects
class Player(CircleShape):
   def __init__(self, x, y):
      super().__init__(x, y, PLAYER_RADIUS)
      self.rotation = 0
      
   # in the player class
   def triangle(self):
      forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Changed from 1 to -1
      right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5  # Changed from 1 to -1
      a = self.position + forward * self.radius
      b = self.position - forward * self.radius - right
      c = self.position - forward * self.radius + right
      return [a, b, c]
      
      # overides func draw(self, screen) in CircleShape class
   def draw(self, screen):
      pygame.draw.polygon(screen, COLOR_WHITE, self.triangle(), PLAYER_POLYGON_LINE_WIDTH)
   
   def rotate(self, dt):
      self.rotation += (PLAYER_TURN_SPEED * dt)
   
   def move(self, dt):
      # Create a unit vector pointing up (0, -1)
      forwardVec = pygame.Vector2(0, -1)  # Changed from 1 to -1
      # Rotate the vector by player's rotation
      direction = forwardVec.rotate(self.rotation)
      # Scale the vector by speed and time
      movement = direction * PLAYER_SPEED * dt
      # Update position
      self.position += movement

   def update(self, dt):
      keys = pygame.key.get_pressed()

      if keys[pygame.K_w]: #Forward Movement
         self.move(dt)
            
      if keys[pygame.K_a] and keys[pygame.K_s]: #Left Rotation & backwards moving
         self.rotate(dt)
      elif keys[pygame.K_a]: #Left Rotation and/or Forward Movement & Left Rotation
         self.rotate(-dt)
 
      if keys[pygame.K_s]: #Backwards Movement
         self.move(-dt)
         
      if keys[pygame.K_d] and keys[pygame.K_s]: #Right Rotation & backwards moving
         self.rotate(-dt)
      elif keys[pygame.K_d]: #Right Rotation and/or Forward Movement & Right Rotation
         self.rotate(dt)