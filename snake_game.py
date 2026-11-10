
import pygame
import numpy as np
import random
import sys

# Initialize Pygame
pygame.init()

# ---------------- GAME SETTINGS ----------------

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

FPS = 10

# Colors (RGB)
BLACK = (15, 15, 15)
GREEN = (0, 255, 100)
DARK_GREEN = (0, 180, 70)
RED = (255, 50, 50)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 220, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Python + NumPy")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 45, bold=True)

# Game Over Buttons
replay_button = pygame.Rect(180, 380, 110, 50)
quit_button = pygame.Rect(320, 380, 110, 50)

# ---------------- GAME VARIABLES ----------------

# Snake starts at the center
snake = [
    (ROWS // 2, COLS // 2),
    (ROWS // 2, COLS // 2 - 1),
    (ROWS // 2, COLS // 2 - 2)
]

# Initial direction: Right
direction = (0, 1)

# Generate random food
def generate_food():

    # Find empty cells using NumPy
    empty_cells = [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) not in snake
    ]

    # Select random empty cell
    if not empty_cells:
        return None

    index = np.random.randint(len(empty_cells))

    return empty_cells[index]


food = generate_food()

score = 0
game_over = False
won = False


# ---------------- DRAW SNAKE ----------------

def draw_snake():

    for index, (row, col) in enumerate(snake):

        x = col * CELL_SIZE
        y = row * CELL_SIZE

        # Head has a different color
        color = GREEN if index == 0 else DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2),
            border_radius=5
        )


# ---------------- DRAW FOOD ----------------

def draw_food():

    if food is not None:

        row, col = food

        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            RED,
            (x, y),
            CELL_SIZE // 2 - 2
        )


# ---------------- DRAW SCORE ----------------

def draw_score():

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))


# ---------------- GAME OVER SCREEN ----------------


def draw_game_over():

    # Game Over heading
    title = big_font.render("GAME OVER", True, RED)

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 220)
    )

    # Final score
    final_score = font.render(
        f"Your Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        final_score,
        (WIDTH // 2 - final_score.get_width() // 2, 290)
    )

    # Draw Replay button
    pygame.draw.rect(
        screen, GREEN, replay_button, border_radius=10
    )

    replay_text = font.render("REPLAY", True, BLACK)

    screen.blit(
        replay_text,
        (replay_button.centerx - replay_text.get_width() // 2,
         replay_button.centery - replay_text.get_height() // 2)
    )

    # Draw Quit button
    pygame.draw.rect(
        screen, RED, quit_button, border_radius=10
    )

    quit_text = font.render("QUIT", True, WHITE)

    screen.blit(
        quit_text,
        (quit_button.centerx - quit_text.get_width() // 2,
         quit_button.centery - quit_text.get_height() // 2)
    )



# ---------------- RESET GAME ----------------

def reset_game():

    global snake, direction, food
    global score, game_over, won, FPS

    snake = [
        (ROWS // 2, COLS // 2),
        (ROWS // 2, COLS // 2 - 1),
        (ROWS // 2, COLS // 2 - 2)
    ]

    direction = (0, 1)

    food = generate_food()

    score = 0
    FPS = 10

    game_over = False
    won = False


# ---------------- MAIN GAME LOOP ----------------

running = True

while running:

    
# Event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:

                # Replay button clicked
                if replay_button.collidepoint(event.pos):
                    reset_game()

                # Quit button clicked
                elif quit_button.collidepoint(event.pos):
                    running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            if game_over:

                if event.key == pygame.K_r:
                    reset_game()

                elif event.key == pygame.K_q:
                    running = False

            else:

                if event.key == pygame.K_UP and direction != (1, 0):
                    direction = (-1, 0)

                elif event.key == pygame.K_DOWN and direction != (-1, 0):
                    direction = (1, 0)

                elif event.key == pygame.K_LEFT and direction != (0, 1):
                    direction = (0, -1)

                elif event.key == pygame.K_RIGHT and direction != (0, -1):
                    direction = (0, 1)


    # ---------------- UPDATE GAME ----------------

    if not game_over:

        # Calculate new head position
        head_row, head_col = snake[0]

        new_head = (
            head_row + direction[0],
            head_col + direction[1]
        )

        # Check wall collision
        if (
            new_head[0] < 0 or
            new_head[0] >= ROWS or
            new_head[1] < 0 or
            new_head[1] >= COLS
        ):
            game_over = True

        else:

            # Check whether food is eaten
            eating = new_head == food

            # Check self collision
            # Moving into the old tail cell is allowed
            # when the snake is not growing.
            body = snake if eating else snake[:-1]

            if new_head in body:
                game_over = True

            else:

                # Add new head
                snake.insert(0, new_head)

                # If food is eaten
                if eating:

                    score += 10

                    # Increase speed
                    FPS = min(25, 10 + score // 50)

                    # Generate new food
                    food = generate_food()

                    # Check if board is completely filled
                    if food is None:
                        game_over = True
                        won = True

                else:

                    # Remove tail to maintain snake length
                    snake.pop()

    # ---------------- DRAW EVERYTHING ----------------

    screen.fill(BLACK)

    # Draw grid
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(
            screen, GRAY, (x, 0), (x, HEIGHT)
        )

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(
            screen, GRAY, (0, y), (WIDTH, y)
        )

    draw_snake()
    draw_food()
    draw_score()

    if game_over:
        draw_game_over()

    # Update display
    pygame.display.update()

    # Control game speed
    clock.tick(FPS)


# Close Pygame
pygame.quit()
sys.exit()
