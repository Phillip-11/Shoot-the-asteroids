import random

import pygame

from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from constants import POWERUP_SPAWN_RATE_SECONDS
from powerup import PowerUp


class PowerUpField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            kind = random.choice(["shield", "speed"])
            x = random.uniform(80, SCREEN_WIDTH - 80)
            y = random.uniform(80, SCREEN_HEIGHT - 80)
            powerup = PowerUp(x, y, kind)
            powerup.velocity = pygame.Vector2(
                random.uniform(-15, 15), random.uniform(-15, 15)
            )
