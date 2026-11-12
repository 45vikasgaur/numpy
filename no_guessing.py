
import numpy as np

# Function to start the game
def start_game():

    print("\n================================")
    print("       NUMBER GUESSING GAME")
    print("================================")

    # Difficulty selection
    print("\nSelect Difficulty:")
    print("1. Easy   (1 - 50) | 10 Attempts")
    print("2. Medium (1 - 100) | 7 Attempts")
    print("3. Hard   (1 - 500) | 5 Attempts")

    level = input("\nChoose Level (1/2/3): ")

    # Set game difficulty
    if level == "1":
        maximum = 50
        chances = 10

    elif level == "2":
        maximum = 100
        chances = 7

    elif level == "3":
        maximum = 500
        chances = 5

    else:
        print("Invalid selection! Defaulting to Easy.")
        maximum = 50
        chances = 10

    # Generate random number
    number = np.random.randint(1, maximum + 1)

    score = 0
    total_attempts = chances

    print(f"\nGuess a number between 1 and {maximum}.")

    # Main game loop
    while chances > 0:

        print("\n--------------------------------")
        print("Attempts Remaining:", chances)

        try:
            guess = int(input("Enter your guess: "))

        except ValueError:
            print("Please enter a valid integer!")
            continue

        if guess < 1 or guess > maximum:
            print(f"Enter a number between 1 and {maximum}.")
            continue

        if guess == number:

            print("\n*** CORRECT GUESS! ***")
            print("You Won the Game!")

            score = chances * 10
            print("Your Score:", score)

            break

        elif guess < number:

            print("Too Low!")

            if number - guess <= 5:
                print("Hint: You are very close!")

        else:

            print("Too High!")

            if guess - number <= 5:
                print("Hint: You are very close!")

        chances -= 1

    # Game over
    if chances == 0:
        print("\nGAME OVER!")
        print("Correct Number Was:", number)
        print("Your Score: 0")

# Main program
while True:

    start_game()

    print("\n================================")
    print("1. Play Again")
    print("2. Quit")
    print("================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nStarting New Game...")

    elif choice == "2":
        print("\nThanks for Playing!")
        print("Game Closed.")
        break

    else:
        print("Invalid Choice! Game Closed.")
        break
