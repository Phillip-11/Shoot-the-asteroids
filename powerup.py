import pygame

from circleshape import CircleShape
from constants import POWERUP_RADIUS
from constants import LINE_WIDTH


class PowerUp(CircleShape):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, kind: str) -> None:
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind  # "shield" or "speed"

    def draw(self, screen: pygame.Surface) -> None:
        color = "cyan" if self.kind == "shield" else "yellow"
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)
        pygame.draw.circle(screen, color, self.position, max(1, self.radius - 4), 1)

    def update(self, dt: float) -> None:
        # power-ups drift slowly instead of sitting perfectly still
        self.position += self.velocity * dt
