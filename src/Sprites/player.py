import pygame
from CONSTS.KEYS import KEY_A, KEY_D, KEY_S, KEY_SPACE, KEY_W
from CONSTS.PLAYER import (
    PLAYER_RADIUS,
    PLAYER_LIVES,
    PLAYER_POLYGON_LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_MOVEMENT_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN
)
from CONSTS.COLORS import COLOR_WHITE, COLOR_GREEN
from CONSTS.SHOTS import SHOT_RADIUS
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
        self.games_played = 0
        self.high_score = 0
        self.lives = PLAYER_LIVES
        self.still_alive = True
        self.level = 1
        self.xp_to_next_level = self.level * 150
        self.xp = 0
        self.xp_bar_percentage = self.xp / self.xp_to_next_level
        self.xp_bar_color = COLOR_GREEN

    def reset(self):
        """Reset the player's state to default values.

        Returns:
            None
        """
        self.position = pygame.Vector2(0, 0)
        self.rotation = 0
        self.timer = 0.0
        self.kill_count = 0
        self.lives = PLAYER_LIVES
        self.still_alive = True

    def triangle(self):
        """Calculate the vertices of the player's triangular shape.

        Returns:
            list: Three pygame.Vector2 points representing the triangle's sides
        """
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Forward vector
        right = (
            pygame.Vector2(0, -1).rotate(self.rotation + 90)
            * self.radius / 1.5
        )  # Changed from 1 to -1
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
        pygame.draw.polygon(
            screen, COLOR_WHITE, self.triangle(), PLAYER_POLYGON_LINE_WIDTH
        )

    def rotate(self, dt):
        """Rotate the player's ship.

        Args:
            dt: float - Delta time since last update

        Returns:
            None
        """
        self.rotation += PLAYER_TURN_SPEED * dt

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
        # Spawn shot at player's current position
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        # Set the shot's velocity in the direction the player is facing
        forwardVec = pygame.Vector2(0, -1)
        # Assuming forward is up (0, -1) towards front of player
        shot.velocity = forwardVec.rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        """Update the player's state based on input and time.

        Handles player movement, rotation, and shooting based on keyboard input.    # noqa: E501

        Args:
            dt: float - Delta time since last update

        Returns:
            None
        """
        keys = pygame.key.get_pressed()
        # Forward Movement
        if keys[KEY_W]:
            self.move(dt)
        # Left Rotation & backwards moving
        if keys[KEY_A] and keys[KEY_S]:
            self.rotate(dt)
        # Left Rotation and/or Forward Movement & Left Rotation
        elif keys[KEY_A]:
            self.rotate(-dt)
        # Backwards Movement
        if keys[KEY_S]:
            self.move(-dt)
        # Right Rotation & backwards moving
        if keys[KEY_S] and keys[KEY_D]:
            self.rotate(-dt)
        # Right Rotation and/or Forward Movement & Right Rotation
        elif keys[KEY_D]:
            self.rotate(dt)

        # Update shot cooldown timer and then shoot
        # if space is pressed and cooldown is over
        if self.timer > 0:
            self.timer -= dt
        elif self.timer < 0:
            self.timer = 0  # reset timer to 0 if we go negative

        if keys[KEY_SPACE]:
            if self.timer > 0:
                pass  # dont shoot
            else:
                self.shoot()
                self.timer = PLAYER_SHOOT_COOLDOWN
