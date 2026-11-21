
import pygame
import numpy as np
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NUMPY NEON SHOOTER")

clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 25)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (180, 0, 255)
RED = (255, 60, 80)
GREEN = (0, 255, 120)

# Fonts
font = pygame.font.SysFont("Arial", 25, bold=True)
big_font = pygame.font.SysFont("Arial", 55, bold=True)

# Player position using NumPy
player = np.array([450.0, 520.0])

player_speed = 6

# Bullets
bullets = []

# Enemies
enemies = []

# Game variables
score = 0
health = 100
level = 1
game_over = False

# Background stars
stars = [
    [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    for _ in range(80)
]


def draw_text(text, x, y, color=WHITE, size_font=font):
    image = size_font.render(str(text), True, color)
    screen.blit(image, (x, y))


def create_enemy():
    x = random.randint(30, WIDTH - 30)

    # NumPy random number generation
    number = np.random.randint(1, 10)

    enemies.append({
        "pos": np.array([float(x), -20.0]),
        "number": number,
        "speed": random.uniform(1.5, 3.0) + level * 0.3
    })


def reset_game():
    global score, health, level, game_over
    global player, bullets, enemies

    score = 0
    health = 100
    level = 1
    game_over = False

    player = np.array([450.0, 520.0])
    bullets = []
    enemies = []


# Enemy creation timer
spawn_timer = 0

running = True

while running:

    clock.tick(60)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(
                    np.array([player[0], player[1] - 25])
                )

            if event.key == pygame.K_r and game_over:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player[0] -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player[0] += player_speed

        player[0] = np.clip(player[0], 20, WIDTH - 20)

        # Draw player
        pygame.draw.polygon(
            screen, CYAN,
            [
                (int(player[0]), int(player[1] - 25)),
                (int(player[0] - 20), int(player[1] + 20)),
                (int(player[0] + 20), int(player[1] + 20))
            ]
        )

        # Bullets movement
        for bullet in bullets[:]:
            bullet[1] -= 9

            pygame.draw.circle(
                screen, GREEN,
                (int(bullet[0]), int(bullet[1])), 5
            )

            if bullet[1] < 0:
                bullets.remove(bullet)

        # Create enemies
        spawn_timer += 1

        if spawn_timer > max(15, 55 - level * 3):
            create_enemy()
            spawn_timer = 0

        # Enemy movement
        for enemy in enemies[:]:

            enemy["pos"][1] += enemy["speed"]

            x = int(enemy["pos"][0])
            y = int(enemy["pos"][1])

            pygame.draw.circle(screen, PURPLE, (x, y), 20)

            draw_text(
                enemy["number"], x - 7, y - 13, WHITE
            )

            # Collision with player
            distance = np.linalg.norm(enemy["pos"] - player)

            if distance < 35:
                health -= 10
                enemies.remove(enemy)
                continue

            # Enemy reaches bottom
            if y > HEIGHT:
                health -= 10
                enemies.remove(enemy)
                continue

            # Bullet collision using NumPy
            for bullet in bullets[:]:

                distance = np.linalg.norm(
                    enemy["pos"] - bullet
                )

                if distance < 25:

                    score += enemy["number"] * 10

                    if enemy in enemies:
                        enemies.remove(enemy)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    break

        # Level system
        level = 1 + score // 200

        # Health
        if health <= 0:
            health = 0
            game_over = True

        # Background stars
        for star in stars:
            star[1] += 2

            if star[1] > HEIGHT:
                star[0] = random.randint(0, WIDTH)
                star[1] = 0

            pygame.draw.circle(
                screen, WHITE,
                (star[0], star[1]), 1
            )

    else:

        draw_text(
            "GAME OVER",
            290, 210, RED, big_font
        )

        draw_text(
            f"Final Score: {score}",
            350, 290, WHITE
        )

        draw_text(
            "Press R to Restart",
            325, 350, GREEN
        )

    # HUD
    draw_text(f"SCORE: {score}", 20, 20, CYAN)
    draw_text(f"LEVEL: {level}", 390, 20, PURPLE)
    draw_text(f"HEALTH: {health}", 730, 20, GREEN)

    # Health bar
    pygame.draw.rect(
        screen, RED, (730, 55, 150, 10)
    )

    pygame.draw.rect(
        screen, GREEN, (730, 55, health * 1.5, 10)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()
