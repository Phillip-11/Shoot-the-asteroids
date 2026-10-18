import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS
from constants import LINE_WIDTH
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_ACCELERATION
from constants import PLAYER_MAX_SPEED
from constants import PLAYER_FRICTION
from constants import PLAYER_SHOOT_SPEED
from constants import PLAYER_SHOOT_COOLDOWN_SECONDS
from constants import HEAVY_SHOT_SPEED
from constants import HEAVY_SHOT_COOLDOWN_SECONDS
from constants import BOMB_COOLDOWN_SECONDS
from constants import SHIELD_DURATION_SECONDS
from constants import SPEED_BOOST_DURATION_SECONDS
from constants import SPEED_BOOST_MULTIPLIER
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from shot import Shot
from bomb import Bomb


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        self.shoot_timer = 0.0
        self.heavy_shoot_timer = 0.0
        self.bomb_timer = 0.0
        self.weapon = "normal"  # "normal" or "heavy"

        self.invulnerable_timer = 0.0
        self.shield_timer = 0.0
        self.speed_boost_timer = 0.0

    def is_invulnerable(self) -> bool:
        return self.invulnerable_timer > 0 or self.shield_timer > 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        # flicker the ship while the post-respawn invulnerability is active
        flickering = self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0
        if not flickering:
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

        if self.shield_timer > 0:
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 6, 2)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_1]:
            self.weapon = "normal"
        if keys[pygame.K_2]:
            self.weapon = "heavy"
        if keys[pygame.K_b]:
            self.drop_bomb()

        self.move(dt)

        self.shoot_timer -= dt
        self.heavy_shoot_timer -= dt
        self.bomb_timer -= dt
        self.invulnerable_timer -= dt
        self.shield_timer -= dt
        self.speed_boost_timer -= dt

        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    def accelerate(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def move(self, dt: float) -> None:
        # drag, so the ship coasts to a stop instead of accelerating forever
        self.velocity *= max(0.0, 1 - PLAYER_FRICTION * dt)

        max_speed = PLAYER_MAX_SPEED
        if self.speed_boost_timer > 0:
            max_speed *= SPEED_BOOST_MULTIPLIER

        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        self.position += self.velocity * dt

    def shoot(self) -> None:
        if self.weapon == "heavy":
            if self.heavy_shoot_timer > 0:
                return
            self.heavy_shoot_timer = HEAVY_SHOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y, heavy=True)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * HEAVY_SHOT_SPEED
        else:
            if self.shoot_timer > 0:
                return
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def drop_bomb(self) -> None:
        if self.bomb_timer > 0:
            return
        self.bomb_timer = BOMB_COOLDOWN_SECONDS
        Bomb(self.position.x, self.position.y)

    def apply_powerup(self, kind: str) -> None:
        if kind == "shield":
            self.shield_timer = SHIELD_DURATION_SECONDS
        elif kind == "speed":
            self.speed_boost_timer = SPEED_BOOST_DURATION_SECONDS

    def respawn(self, x: float, y: float, invulnerable_seconds: float) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = invulnerable_seconds

    def collides_with(self, other) -> bool:
        # the ship uses its triangular shape instead of a circle for collisions
        a, b, c = self.triangle()

        if self._point_in_triangle(other.position, a, b, c):
            return True

        for p1, p2 in ((a, b), (b, c), (c, a)):
            if self._segment_distance(other.position, p1, p2) <= other.radius:
                return True

        return False

    @staticmethod
    def _point_in_triangle(p, a, b, c) -> bool:
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)

        has_neg = d1 < 0 or d2 < 0 or d3 < 0
        has_pos = d1 > 0 or d2 > 0 or d3 > 0

        return not (has_neg and has_pos)

    @staticmethod
    def _segment_distance(p, a, b) -> float:
        ab = b - a
        if ab.length_squared() == 0:
            return p.distance_to(a)
        t = max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared()))
        closest = a + ab * t
        return p.distance_to(closest)
