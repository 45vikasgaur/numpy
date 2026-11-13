
import numpy as np
import random
import os
import json

# ==============================
# PREMIUM 2048 GAME
# Python + NumPy
# ==============================

BEST_FILE = "best_score.json"

# Load best score
def load_best():
    try:
        with open(BEST_FILE, "r") as f:
            return json.load(f).get("best", 0)
    except:
        return 0

# Save best score
def save_best(score):
    with open(BEST_FILE, "w") as f:
        json.dump({"best": score}, f)


best_score = load_best()
score = 0
board = np.zeros((4, 4), dtype=int)
history = []

# Colors
COLORS = {
    0: "\033[90m",
    2: "\033[97m",
    4: "\033[96m",
    8: "\033[92m",
    16: "\033[93m",
    32: "\033[94m",
    64: "\033[95m",
    128: "\033[91m",
    256: "\033[96m",
    512: "\033[92m",
    1024: "\033[93m",
    2048: "\033[97m"
}

RESET = "\033[0m"
BOLD = "\033[1m"


# Add random tile
def add_tile():
    empty = list(zip(*np.where(board == 0)))

    if empty:
        r, c = random.choice(empty)
        board[r][c] = random.choices(
            [2, 4], weights=[90, 10]
        )[0]


# Display board
def display():
    os.system("cls" if os.name == "nt" else "clear")

    print("\n" + "=" * 45)
    print("          ✦ 2048 PREMIUM PRO ✦")
    print("=" * 45)

    print(f"\n  SCORE: {score}")
    print(f"  BEST : {best_score}")

    print("\n" + "-" * 37)

    for row in board:
        print("|", end="")

        for value in row:
            color = COLORS.get(value, "\033[97m")

            if value == 0:
                text = "    "
            else:
                text = f"{value:^4}"

            print(f"{color}{BOLD}{text}{RESET}|", end="")

        print("\n" + "-" * 37)

    print("\n  W = UP       S = DOWN")
    print("  A = LEFT     D = RIGHT")
    print("  U = UNDO     R = RESTART")
    print("  Q = QUIT")
    print("=" * 45)


# Merge one row towards left
def merge_left(row):
    global score

    numbers = row[row != 0]
    merged = []

    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            value = numbers[i] * 2
            merged.append(value)
            score += value
            i += 2
        else:
            merged.append(numbers[i])
            i += 1

    return np.array(
        merged + [0] * (4 - len(merged))
    )


# Move board
def move(direction):
    global board, score

    old_board = board.copy()
    old_score = score

    if direction == "a":
        for i in range(4):
            board[i] = merge_left(board[i])

    elif direction == "d":
        for i in range(4):
            board[i] = merge_left(board[i][::-1])[::-1]

    elif direction == "w":
        board = board.T
        for i in range(4):
            board[i] = merge_left(board[i])
        board = board.T

    elif direction == "s":
        board = board.T
        for i in range(4):
            board[i] = merge_left(board[i][::-1])[::-1]
        board = board.T

    if not np.array_equal(old_board, board):
        history.append((old_board, old_score))
        add_tile()
        return True

    return False


# Undo
def undo():
    global board, score

    if history:
        board, score = history.pop()
        return True

    return False


# Check game over
def game_over():
    if np.any(board == 0):
        return False

    for i in range(4):
        for j in range(4):
            if j < 3 and board[i][j] == board[i][j+1]:
                return False

            if i < 3 and board[i][j] == board[i+1][j]:
                return False

    return True


# New game
def new_game():
    global board, score, history

    board = np.zeros((4, 4), dtype=int)
    score = 0
    history = []

    add_tile()
    add_tile()


# Main game
def main():

    global score, best_score

    new_game()

    while True:

        display()

        if np.any(board >= 2048):
            print("\n🏆 CONGRATULATIONS! YOU REACHED 2048!")
            print("Continue playing or restart.")
        
        if game_over():
            print("\n💀 GAME OVER!")
            print("Final Score:", score)

            if score > best_score:
                best_score = score
                save_best(best_score)
                print("🏆 NEW HIGH SCORE!")

            choice = input("\nR = Replay | Q = Quit: ").lower()

            if choice == "r":
                new_game()
                continue
            elif choice == "q":
                break
            else:
                continue

        key = input("\nEnter move: ").lower()

        if key in ["w", "a", "s", "d"]:
            move(key)

        elif key == "u":
            undo()

        elif key == "r":
            confirm = input("Restart game? (y/n): ").lower()
            if confirm == "y":
                new_game()

        elif key == "q":
            print("\nThanks for playing 2048 Premium!")
            break

        if score > best_score:
            best_score = score
            save_best(best_score)


if __name__ == "__main__":
    main()
