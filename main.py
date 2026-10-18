import random
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from bomb import Bomb
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from constants import PLAYER_LIVES
from constants import PLAYER_RESPAWN_INVULNERABLE_SECONDS
from constants import ASTEROID_MIN_RADIUS
from constants import SCORE_LARGE_ASTEROID
from constants import SCORE_MEDIUM_ASTEROID
from constants import SCORE_SMALL_ASTEROID
from constants import BOMB_BLAST_RADIUS
from constants import STAR_COUNT
from explosion import Explosion
from logger import log_state
from logger import log_event
from player import Player
from powerup import PowerUp
from powerupfield import PowerUpField
from shot import Shot


def score_for_radius(radius: float) -> int:
    # smaller asteroids are harder to hit, so they're worth more
    if radius > ASTEROID_MIN_RADIUS * 2:
        return SCORE_LARGE_ASTEROID
    if radius > ASTEROID_MIN_RADIUS:
        return SCORE_MEDIUM_ASTEROID
    return SCORE_SMALL_ASTEROID


def make_starfield(count: int) -> list[tuple[int, int, int]]:
    stars = []
    for _ in range(count):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        brightness = random.randint(80, 200)
        stars.append((x, y, brightness))
    return stars


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    dt = 0.0

    stars = make_starfield(STAR_COUNT)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = updatable
    AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    bombs = pygame.sprite.Group()
    Bomb.containers = (bombs, updatable, drawable)

    explosions = pygame.sprite.Group()
    Explosion.containers = (explosions, updatable, drawable)

    powerups = pygame.sprite.Group()
    PowerUp.containers = (powerups, updatable, drawable)
    PowerUpField.containers = updatable
    PowerUpField()

    score = 0
    lives = PLAYER_LIVES

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if not player.is_invulnerable() and player.collides_with(asteroid):
                log_event("player_hit")
                Explosion(player.position.x, player.position.y)
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    print(f"Final score: {score}")
                    sys.exit()
                player.respawn(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                    PLAYER_RESPAWN_INVULNERABLE_SECONDS,
                )
                break

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += score_for_radius(asteroid.radius)
                    Explosion(asteroid.position.x, asteroid.position.y)
                    if getattr(shot, "heavy", False):
                        asteroid.kill()
                    else:
                        asteroid.split()
                    break

        for bomb in list(bombs):
            if bomb.exploded:
                log_event("bomb_exploded")
                Explosion(bomb.position.x, bomb.position.y)
                for asteroid in list(asteroids):
                    if asteroid.position.distance_to(bomb.position) <= BOMB_BLAST_RADIUS:
                        score += score_for_radius(asteroid.radius)
                        asteroid.split()
                bomb.kill()

        for powerup in list(powerups):
            if player.collides_with(powerup):
                log_event("powerup_collected", kind=powerup.kind)
                player.apply_powerup(powerup.kind)
                powerup.kill()

        screen.fill("black")
        for sx, sy, brightness in stars:
            screen.set_at((sx, sy), (brightness, brightness, brightness))

        for drawable_obj in drawable:
            drawable_obj.draw(screen)

        hud_text = f"Score: {score}   Lives: {lives}   Weapon: {player.weapon}"
        hud = font.render(hud_text, True, "white")
        screen.blit(hud, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
