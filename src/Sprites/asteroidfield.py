import pygame
import random
from Sprites.asteroid import Asteroid
from CONSTS.ASTEROIDS import (
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    ASTEROID_SPAWN_RATE
)
from CONSTS.SCREEN import SCREEN_WIDTH, SCREEN_HEIGHT


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        """Initialize the asteroid field manager.

        Sets up the sprite container and initializes the spawn timer for creating new asteroids.

        Returns:
            None
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        """Create a new asteroid with specified parameters.

        Args:
            radius: float - The radius of the new asteroid
            position: pygame.Vector2 - The spawn position of the asteroid
            velocity: pygame.Vector2 - The initial velocity vector of the asteroid

        Returns:
            None
        """
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        """Update the asteroid field state and spawn new asteroids.

        Manages the asteroid spawn timer and creates new asteroids at random edges
        of the screen with random properties when the timer expires.

        Args:
            dt: float - Delta time since last update

        Returns:
            None
        """
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
