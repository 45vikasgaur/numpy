
import numpy as np

# Number Prediction Game
print("=" * 45)
print("       NUMBER PREDICTION GAME")
print("=" * 45)

# Game instructions
print("\nWelcome to the Number Prediction Game!")
print("I have selected a random number between 1 and 100.")
print("You have 7 chances to guess the correct number.")

# Generate random number using NumPy
secret_number = np.random.randint(1, 101)

# Game variables
attempts = 7
score = 0

# Game loop
while attempts > 0:

    print("\n-----------------------------------")
    print("Remaining chances:", attempts)

    try:
        guess = int(input("Enter your prediction: "))

    except ValueError:
        print("Invalid input! Please enter a number.")
        continue

    # Check input range
    if guess < 1 or guess > 100:
        print("Please enter a number between 1 and 100.")
        continue

    # Check prediction
    if guess == secret_number:

        print("\nCongratulations! You guessed correctly!")
        score = attempts * 10
        break

    elif guess < secret_number:

        print("Too Low! Try a bigger number.")

    else:

        print("Too High! Try a smaller number.")

    attempts -= 1

# Game over condition
if attempts == 0:
    print("\nGAME OVER!")
    print("The correct number was:", secret_number)

# Display score
print("\nYour Final Score:", score)

# Replay option
while True:

    print("\n===================================")
    print("1. Play Again")
    print("2. Quit")
    print("===================================")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":

        print("\nRestarting Game...\n")

        # Start a new game
        secret_number = np.random.randint(1, 101)
        attempts = 7
        score = 0

        while attempts > 0:

            print("\nRemaining chances:", attempts)

            try:
                guess = int(input("Enter your prediction: "))
            except ValueError:
                print("Invalid input! Enter a number.")
                continue

            if guess < 1 or guess > 100:
                print("Enter a number between 1 and 100.")
                continue

            if guess == secret_number:
                print("\nCorrect Prediction!")
                score = attempts * 10
                break

            elif guess < secret_number:
                print("Too Low!")

            else:
                print("Too High!")

            attempts -= 1

        if attempts == 0:
            print("\nGAME OVER!")
            print("Correct Number:", secret_number)

        print("Your Final Score:", score)

    elif choice == "2":

        print("\nThanks for playing!")
        print("Game Closed.")
        break

    else:
        print("Invalid choice! Select 1 or 2.")
