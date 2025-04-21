import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
   def __init__(self, x, y, radius):
      # we will be using this later
      if hasattr(self, "containers"):
         super().__init__(self.containers)
      else:
         super().__init__()

      self.position = pygame.Vector2(x, y)
      self.velocity = pygame.Vector2(0, 0)
      self.radius = radius

   def draw(self, screen):
      # sub-classes must override
      pass

   def update(self, dt):
      # sub-classes must override
      pass

   def colliding_with(self, other: "CircleShape") -> bool:
      distance = pygame.Vector2.distance_to(self.position, other.position)
      # Get the radii of both circles
      r1 = self.radius
      r2 = other.radius
      
       # Compare the distance with the combined radii
      return distance <= (r1 + r2) # Return True if colliding, False otherwise