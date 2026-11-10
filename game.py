
import numpy as np

# Create a 3x3 game board using NumPy
board = np.full((3, 3), " ", dtype="<U1")


# Function to display the board
def display_board():
    print("\n   1   2   3")
    for i in range(3):
        print(f"{i + 1}  " + " | ".join(board[i]))
        if i < 2:
            print("  ---+---+---")
    print()


# Function to check the winner
def check_winner(player):

    # Check all rows
    for row in board:
        if np.all(row == player):
            return True

    # Check all columns
    for col in board.T:
        if np.all(col == player):
            return True

    # Check both diagonals
    if np.all(np.diag(board) == player):
        return True

    if np.all(np.diag(np.fliplr(board)) == player):
        return True

    return False


# Function to check if board is full
def is_draw():
    return not np.any(board == " ")


# Player move
def player_move():
    while True:
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1

            if 0 <= row < 3 and 0 <= col < 3:
                if board[row, col] == " ":
                    board[row, col] = "X"
                    break
                else:
                    print("Position already taken!")
            else:
                print("Enter numbers between 1 and 3.")

        except ValueError:
            print("Please enter valid numbers.")


# Computer move using NumPy
def computer_move():

    # Find all empty positions
    empty_cells = np.argwhere(board == " ")

    # Select a random empty position
    random_index = np.random.randint(len(empty_cells))

    row, col = empty_cells[random_index]

    board[row, col] = "O"

    print(f"Computer played: {row + 1}, {col + 1}")


# Main game function
def play_game():

    global board

    board = np.full((3, 3), " ", dtype="<U1")

    print("WELCOME TO TIC TAC TOE")
    print("You = X | Computer = O")

    while True:

        display_board()

        # Human turn
        player_move()

        if check_winner("X"):
            display_board()
            print("Congratulations! You Win!")
            break

        if is_draw():
            display_board()
            print("Game Draw!")
            break

        # Computer turn
        computer_move()

        if check_winner("O"):
            display_board()
            print("Computer Wins!")
            break

        if is_draw():
            display_board()
            print("Game Draw!")
            break


# Start game
while True:

    play_game()

    again = input("Play again? (yes/no): ").lower()

    if again != "yes":
        print("Thanks for playing!")
        break
