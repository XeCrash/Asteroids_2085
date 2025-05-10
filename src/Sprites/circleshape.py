import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        """Initialize a circular game object.

        Args:
            x: float - Initial x-coordinate position
            y: float - Initial y-coordinate position
            radius: float - Radius of the circular object

        Returns:
            None
        """
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        """Draw the circular object on the screen.

        Args:
            screen: pygame.Surface - The surface to draw on

        Returns:
            None

        Note:
            This is an abstract method that must be overridden by subclasses.
        """
        # sub-classes must override
        pass

    def update(self, dt):
        """Update the object's state.

        Args:
            dt: float - Delta time since last update

        Returns:
            None

        Note:
            This is an abstract method that must be overridden by subclasses.
        """
        # sub-classes must override
        pass

    def colliding_with(self, other: "CircleShape") -> bool:
        """Check if this object is colliding with another circular object.

        Args:
            other: CircleShape - The other circular object to check collision with

        Returns:
            bool: True if objects are colliding, False otherwise

        Note:
            This method uses the distance formula to check for collision.
        """
        distance = pygame.Vector2.distance_to(self.position, other.position)
        # Get the radii of both circles
        r1 = self.radius
        r2 = other.radius

        # Compare the distance with the combined radii
        return distance <= (r1 + r2)  # Return True if colliding, False otherwise
