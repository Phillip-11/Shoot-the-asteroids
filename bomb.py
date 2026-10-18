import pygame

from circleshape import CircleShape
from constants import BOMB_RADIUS
from constants import BOMB_FUSE_SECONDS
from constants import LINE_WIDTH


class Bomb(CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, BOMB_RADIUS)
        self.fuse = BOMB_FUSE_SECONDS
        self.exploded = False

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.fuse -= dt
        if self.fuse <= 0 and not self.exploded:
            self.exploded = True
