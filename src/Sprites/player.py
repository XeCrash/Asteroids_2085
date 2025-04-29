import pygame
from CONSTS.PLAYER import *
from CONSTS.COLORS import *
from CONSTS.SHOTS import *
from Sprites.circleshape import CircleShape
from Sprites.shot import Shot


# Base class for player objects
class Player(CircleShape):
   def __init__(self, x, y):
      """Initialize the player object.
      
      Args:
          x: float - Initial x-coordinate position
          y: float - Initial y-coordinate position
          
      Returns:
          None
      """
      super().__init__(x, y, PLAYER_RADIUS)
      self.rotation = 0
      self.timer = 0.0
      self.kill_count = 0
      
   # in the player class
   def triangle(self):
      """Calculate the vertices of the player's triangular shape.
      
      Returns:
          list: Three pygame.Vector2 points representing the triangle vertices
      """
      forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Changed from 1 to -1
      right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5  # Changed from 1 to -1
      a = self.position + forward * self.radius
      b = self.position - forward * self.radius - right
      c = self.position - forward * self.radius + right
      return [a, b, c]
      
      # overrides func draw(self, screen) in CircleShape class
   def draw(self, screen):
      """Render the player's triangular ship on the screen.
      
      Args:
          screen: pygame.Surface - The surface to draw the player on
          
      Returns:
          None
      """
      pygame.draw.polygon(screen, COLOR_WHITE, self.triangle(), PLAYER_POLYGON_LINE_WIDTH)
   
   def rotate(self, dt):
      """Rotate the player's ship.
      
      Args:
          dt: float - Delta time since last update
          
      Returns:
          None
      """
      self.rotation += (PLAYER_TURN_SPEED * dt)
   
   def move(self, dt):
      """Move the player's ship in its current direction.
      
      Args:
          dt: float - Delta time since last update
          
      Returns:
          None
      """
      # Create a unit vector pointing up (0, -1)
      forwardVec = pygame.Vector2(0, -1)  # Changed from 1 to -1
      # Rotate the vector by player's rotation
      direction = forwardVec.rotate(self.rotation)
      # Scale the vector by speed and time
      movement = direction * PLAYER_MOVEMENT_SPEED * dt
      # Update position
      self.position += movement
      
   def shoot(self):
      """Create a new shot projectile in the direction the player is facing.
      
      Returns:
          None
      """
      shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
      shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED


   def update(self, dt):
      """Update the player's state based on input and time.
      
      Handles player movement, rotation, and shooting based on keyboard input.
      
      Args:
          dt: float - Delta time since last update
          
      Returns:
          None
      """
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
         
      if self.timer > 0:
         self.timer -= dt
      elif self.timer < 0:
         self.timer = 0 # make sure we normalize it back to 0 incase we go negative 
         
      if keys[pygame.K_SPACE]:
         if self.timer > 0:
            pass # dont shoot
         else:
            self.shoot()
            self.timer = PLAYER_SHOOT_COOLDOWN