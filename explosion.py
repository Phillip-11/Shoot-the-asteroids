import pygame

from constants import EXPLOSION_DURATION_SECONDS


class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float) -> None:
        pygame.sprite.Sprite.__init__(self, *self.containers)
        self.position = pygame.Vector2(x, y)
        self.timer = EXPLOSION_DURATION_SECONDS
        self.max_time = EXPLOSION_DURATION_SECONDS

    def update(self, dt: float) -> None:
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        progress = 1 - max(0.0, self.timer / self.max_time)
        radius = int(6 + progress * 34)
        alpha = max(0, 255 - int(progress * 255))

        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 180, 60, alpha), (radius, radius), radius, 2)
        pygame.draw.circle(
            surface, (255, 80, 20, alpha // 2), (radius, radius), max(1, radius // 2)
        )
        screen.blit(surface, (self.position.x - radius, self.position.y - radius))
