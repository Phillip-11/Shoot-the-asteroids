import random

import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_event

NUM_LUMP_POINTS = 10


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        # random "lumpiness" so the asteroid isn't a perfect circle,
        # computed once so the shape stays stable between frames
        self._lump_scales = [random.uniform(0.75, 1.15) for _ in range(NUM_LUMP_POINTS)]

    def _lumpy_points(self) -> list[pygame.Vector2]:
        points = []
        step = 360 / len(self._lump_scales)
        for i, scale in enumerate(self._lump_scales):
            offset = pygame.Vector2(0, -1).rotate(step * i) * self.radius * scale
            points.append(self.position + offset)
        return points

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self._lumpy_points(), LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        # wrap around the screen edges instead of flying off forever
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT, margin=ASTEROID_MAX_RADIUS)

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(angle)
        velocity_b = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = velocity_a * 1.2

        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b.velocity = velocity_b * 1.2
