# type: ignore
# flake8: noqa
import random


class Game:
    """
    A generic Game base class.

    Initializes the number of attempts for the game and a play method, which is supposed to be implemented by subclasses.
    """

    def __init__(self, attempts):
        self.attempts = attempts

    def play(self):
        raise NotImplementedError("Subclasses must implement this method.")


class GuessTheNumberGame(Game):
    """
    A number guessing game. The player must guess a number between 1 and 100.

    This class inherits from Game.
    Represents a number guessing game where the player tries to guess a randomly chosen number between 1 and 100.
    The __init__ method initializes the number of attempts and generates a random number between 1 and 100.
    """

    def __init__(self, attempts=10):
        """
        Initialize the game with a number of attempts and a randomly chosen number between 1 and 100.
        """
        super().__init__(attempts)
        self.correct_number = random.randint(1, 100)

    def play(self):
        """
        Play the game.

        This method contains the main game loop. It prompts the player to input a guess and then calls the process_guess method to evaluate the guess.
        The loop continues until the player runs out of attempts.
        """
        while self.attempts > 0:
            guess = input("Guess a number between 1 and 100: ")
            if guess.isdigit():
                self.process_guess(int(guess))
            else:
                print("That's not a valid number! Try again.")

        print("Sorry, you didn't guess the number. Better luck next time!")

    def process_guess(self, guess):
        """
        Compares the player's guess with the correct number.
        If the guess is too high or too low, gives feedback to the player.
        If the guess is correct, it congratulates the player and ends the game by setting the remaining attempts to 0.
        After each guess, decrements the number of attempts and prints how many attempts are left.
        """
        if guess > self.correct_number:
            print("Too high!")
        elif guess < self.correct_number:
            print("Too low!")
        else:
            print("Congratulations! You guessed correctly.")
            self.attempts = 0  # end the game

        self.attempts -= 1
        print(f"You have {self.attempts} attempts left.")


# Run the game
game = GuessTheNumberGame()
game.play()
