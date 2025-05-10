import pygame
from Sprites.circleshape import CircleShape
from CONSTS.COLORS import COLOR_YELLOW
from CONSTS.SHOTS import SHOT_LIFETIME


class Shot(CircleShape):
    def __init__(self, x, y, radius):
        """Initialize a shot projectile.

        Args:
            x: float - Initial x-coordinate position
            y: float - Initial y-coordinate position
            radius: float - Radius of the shot projectile

        Returns:
            None
        """
        super().__init__(x, y, radius)
        self.lifetime = 0.0  # Track how long the shot has existed

    def draw(self, screen):
        """Render the shot projectile on the screen.

        Args:
            screen: pygame.Surface - The surface to draw the shot on

        Returns:
            None
        """
        # Draw a solid yellow circle for the shot, circleshape makes collisions easier to detect
        pygame.draw.circle(
            screen, COLOR_YELLOW, [self.position.x, self.position.y], self.radius
        )

    def update(self, dt):
        """Update the shot's position and lifetime.

        Removes the shot if it exceeds its lifetime duration. Updates position
        based on velocity and time delta.

        Args:
            dt: float - Delta time since last update

        Returns:
            None
        """
        self.lifetime += dt
        if self.lifetime >= SHOT_LIFETIME:
            self.kill()
            return

        self.position += self.velocity * dt
