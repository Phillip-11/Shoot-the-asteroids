# Asteroids

A classic Asteroids clone built in Python with [pygame](https://www.pygame.org/), created as part of the [Boot.dev](https://www.boot.dev) backend/game-dev curriculum.

## Gameplay

Pilot a small ship through an endless field of asteroids. Shoot them to break them apart, dodge the debris, grab power-ups, and rack up as high a score as you can before you run out of lives.

- **Large asteroids** split into two **medium** asteroids when destroyed
- **Medium asteroids** split into two **small** asteroids
- **Small asteroids** are destroyed for good
- Smaller asteroids are worth more points — they're harder to hit
- Objects wrap around the screen edges instead of flying off into nowhere
- Get hit without a shield and you lose a life; run out of lives and it's game over

## Controls

| Key | Action |
| --- | --- |
| `A` / `D` | Rotate left / right |
| `W` / `S` | Accelerate forward / backward |
| `Space` | Fire the currently selected weapon |
| `1` | Switch to the standard weapon |
| `2` | Switch to the heavy weapon (slower fire rate, destroys an asteroid outright instead of splitting it) |
| `B` | Drop a bomb (explodes after a short fuse, damaging everything in its blast radius) |

## Features

- Physics-based ship movement with acceleration, drag, and a max speed
- Procedurally "lumpy" asteroid shapes instead of plain circles
- A triangular hitbox for the ship (instead of a bounding circle)
- Two weapon types: a fast standard shot and a slower heavy shot
- Droppable bombs with an area-of-effect blast
- Shield and speed power-ups that spawn periodically
- Explosion effects, a scrolling star background, lives, respawning with brief invulnerability, and an on-screen HUD (score, lives, current weapon)

## Running the game

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
uv run main.py
```

## Tech stack

- Python 3.13
- [pygame](https://www.pygame.org/)
