import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS
from constants import HEAVY_SHOT_RADIUS
from constants import LINE_WIDTH
from constants import SHOT_LIFETIME_SECONDS


class Shot(CircleShape):
    def __init__(self, x, y, heavy: bool = False) -> None:
        self.heavy = heavy
        radius = HEAVY_SHOT_RADIUS if heavy else SHOT_RADIUS
        super().__init__(x, y, radius)
        self.lifetime = SHOT_LIFETIME_SECONDS

    def draw(self, screen: pygame.Surface) -> None:
        color = "orange" if self.heavy else "white"
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
