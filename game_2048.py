
import pygame
import numpy as np
import random
import sys

# Initialize Pygame
pygame.init()

# ---------------- GAME SETTINGS ----------------

WIDTH = 500
HEIGHT = 650

GRID_SIZE = 4
CELL_SIZE = 100
GAP = 10

BOARD_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GAP

# Game colors
BACKGROUND = (250, 248, 239)
BOARD_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TEXT_COLOR = (70, 65, 60)
WHITE = (255, 255, 255)

# Tile colors
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Puzzle Game")

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Arial", 55, bold=True)
font = pygame.font.SysFont("Arial", 35, bold=True)
small_font = pygame.font.SysFont("Arial", 23)
button_font = pygame.font.SysFont("Arial", 25, bold=True)


# ---------------- GAME VARIABLES ----------------

# NumPy 4x4 board
board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

score = 0
best_score = 0

game_over = False
won = False

# Buttons
replay_button = pygame.Rect(105, 410, 130, 50)
quit_button = pygame.Rect(265, 410, 130, 50)


# ---------------- ADD RANDOM TILE ----------------

def add_random_tile():

    # Find all empty cells
    empty_cells = np.argwhere(board == 0)

    # No empty cells available
    if len(empty_cells) == 0:
        return

    # Select random empty position
    index = np.random.randint(len(empty_cells))

    row, col = empty_cells[index]

    # Generate 2 (90%) or 4 (10%)
    board[row, col] = random.choices(
        [2, 4],
        weights=[90, 10]
    )[0]


# ---------------- MERGE ROW ----------------

def merge_row(row):

    global score

    # Remove all zero values
    numbers = [x for x in row if x != 0]

    result = []
    i = 0

    while i < len(numbers):

        # Check whether adjacent numbers are equal
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:

            # Merge two equal numbers
            merged = numbers[i] * 2

            result.append(merged)

            # Increase score
            score += merged

            # Skip the second merged number
            i += 2

        else:

            result.append(numbers[i])
            i += 1

    # Fill remaining positions with zero
    result += [0] * (GRID_SIZE - len(result))

    return result


# ---------------- MOVE LEFT ----------------

def move_left():

    global board

    old_board = board.copy()

    for row in range(GRID_SIZE):

        board[row] = merge_row(board[row].tolist())

    return not np.array_equal(old_board, board)


# ---------------- MOVE RIGHT ----------------

def move_right():

    global board

    old_board = board.copy()

    # Reverse each row
    board = np.fliplr(board).copy()

    move_left()

    # Reverse again
    board = np.fliplr(board).copy()

    return not np.array_equal(old_board, board)


# ---------------- MOVE UP ----------------

def move_up():

    global board

    old_board = board.copy()

    # Transpose rows and columns
    board = board.T.copy()

    move_left()

    # Restore original orientation
    board = board.T.copy()

    return not np.array_equal(old_board, board)


# ---------------- MOVE DOWN ----------------

def move_down():

    global board

    old_board = board.copy()

    # Transpose and reverse
    board = np.fliplr(board.T).copy()

    move_left()

    # Restore original orientation
    board = np.fliplr(board).T.copy()

    return not np.array_equal(old_board, board)


# ---------------- CHECK GAME OVER ----------------

def check_game_over():

    # If empty cells exist, game is not over
    if np.any(board == 0):
        return False

    # Check horizontal matching tiles
    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE - 1):

            if board[row, col] == board[row, col + 1]:
                return False

    # Check vertical matching tiles
    for row in range(GRID_SIZE - 1):

        for col in range(GRID_SIZE):

            if board[row, col] == board[row + 1, col]:
                return False

    return True


# ---------------- CHECK WIN ----------------

def check_win():

    return np.any(board >= 2048)


# ---------------- RESET GAME ----------------

def reset_game():

    global board, score, game_over, won

    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    score = 0
    game_over = False
    won = False

    # Generate two starting tiles
    add_random_tile()
    add_random_tile()


# ---------------- DRAW BOARD ----------------

def draw_board():

    # Draw background
    screen.fill(BACKGROUND)

    # Draw title
    title = title_font.render("2048", True, TEXT_COLOR)

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 15)
    )

    # Display score
    score_text = small_font.render(
        f"Score: {score}    Best: {best_score}",
        True,
        TEXT_COLOR
    )

    screen.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 85)
    )

    # Draw game board background
    board_x = (WIDTH - BOARD_WIDTH) // 2
    board_y = 145

    pygame.draw.rect(
        screen,
        BOARD_COLOR,
        (board_x, board_y, BOARD_WIDTH, BOARD_WIDTH),
        border_radius=8
    )

    # Draw 4x4 cells
    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            value = board[row, col]

            x = board_x + GAP + col * (CELL_SIZE + GAP)
            y = board_y + GAP + row * (CELL_SIZE + GAP)

            # Empty cell color
            if value == 0:
                color = EMPTY_COLOR

            else:
                color = TILE_COLORS.get(
                    int(value),
                    (60, 58, 50)
                )

            # Draw tile
            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE),
                border_radius=6
            )

            # Draw tile number
            if value != 0:

                text_color = (
                    TEXT_COLOR if value <= 4 else WHITE
                )

                tile_font = pygame.font.SysFont(
                    "Arial",
                    35 if value < 1000 else 27,
                    bold=True
                )

                number = tile_font.render(
                    str(value),
                    True,
                    text_color
                )

                screen.blit(
                    number,
                    (
                        x + CELL_SIZE // 2 - number.get_width() // 2,
                        y + CELL_SIZE // 2 - number.get_height() // 2
                    )
                )

    # Instructions
    instruction = small_font.render(
        "Use Arrow Keys to Move Tiles",
        True,
        TEXT_COLOR
    )

    screen.blit(
        instruction,
        (WIDTH // 2 - instruction.get_width() // 2, 570)
    )

    # Display win message
    if won and not game_over:

        win_text = small_font.render(
            "2048 REACHED! Keep playing!",
            True,
            (0, 140, 70)
        )

        screen.blit(
            win_text,
            (WIDTH // 2 - win_text.get_width() // 2, 610)
        )


# ---------------- GAME OVER SCREEN ----------------

def draw_game_over():

    # Dark transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    # Game over title
    title = title_font.render(
        "GAME OVER",
        True,
        WHITE
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 260)
    )

    # Final score
    final_score = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        final_score,
        (WIDTH // 2 - final_score.get_width() // 2, 335)
    )

    # Replay button
    pygame.draw.rect(
        screen,
        (40, 180, 90),
        replay_button,
        border_radius=8
    )

    replay_text = button_font.render(
        "REPLAY",
        True,
        WHITE
    )

    screen.blit(
        replay_text,
        (
            replay_button.centerx - replay_text.get_width() // 2,
            replay_button.centery - replay_text.get_height() // 2
        )
    )

    # Quit button
    pygame.draw.rect(
        screen,
        (220, 60, 60),
        quit_button,
        border_radius=8
    )

    quit_text = button_font.render(
        "QUIT",
        True,
        WHITE
    )

    screen.blit(
        quit_text,
        (
            quit_button.centerx - quit_text.get_width() // 2,
            quit_button.centery - quit_text.get_height() // 2
        )
    )


# ---------------- INITIALIZE GAME ----------------

reset_game()

running = True


# ---------------- MAIN GAME LOOP ----------------

while running:

    # Handle events
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:

            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN and not game_over:

            moved = False

            if event.key == pygame.K_LEFT:

                moved = move_left()

            elif event.key == pygame.K_RIGHT:

                moved = move_right()

            elif event.key == pygame.K_UP:

                moved = move_up()

            elif event.key == pygame.K_DOWN:

                moved = move_down()

            # Add new tile only after a successful move
            if moved:

                add_random_tile()

                # Update best score
                best_score = max(best_score, score)

                # Check for 2048
                if check_win():

                    won = True

                # Check game over
                if check_game_over():

                    game_over = True

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:

                # Replay button
                if replay_button.collidepoint(event.pos):

                    reset_game()

                # Quit button
                elif quit_button.collidepoint(event.pos):

                    running = False

        # Keyboard restart and quit
        if event.type == pygame.KEYDOWN and game_over:

            if event.key == pygame.K_r:

                reset_game()

            elif event.key == pygame.K_q:

                running = False

    # Draw game
    draw_board()

    # Draw game over screen
    if game_over:

        draw_game_over()

    # Update display
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)


# ---------------- CLOSE GAME ----------------

pygame.quit()
sys.exit()
# Key	Action
# ↑ Up Arrow	Move tiles upward
# ↓ Down Arrow	Move tiles downward
# ← Left Arrow	Move tiles left
# → Right Arrow	Move tiles right
# R	Restart after Game Over
# Q	Quit after Game Over
# Mouse click	Replay / Quit buttons