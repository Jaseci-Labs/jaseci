```python
import random


class Game:
    """
    A generic Game base class.
    """

    def __init__(self, attempts):
        self.attempts = attempts

    def play(self):
        raise NotImplementedError("Subclasses must implement this method.")


class GuessTheNumberGame(Game):
    """
    A number guessing game. The player must guess a number between 1 and 100.
    """

    def __init__(self, attempts=10):
        super().__init__(attempts)
        self.correct_number = random.randint(1, 100)

    def play(self):
        while self.attempts > 0:
            guess = input("Guess a number between 1 and 100: ")
            if guess.isdigit():
                self.process_guess(int(guess))
            else:
                print("That's not a valid number! Try again.")

        print("Sorry, you didn't guess the number. Better luck next time!")

    def process_guess(self, guess):
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
```

```jac
"""A Number Guessing Game"""
import:py random;

"""
A generic Game base class.
"""
object Game {
    can init(attempts: int) {
        <self>.attempts = attempts;
    }

    can play() {
        raise NotImplementedError("Subclasses must implement this method.");
    }
}

"""
A number guessing game. The player must guess a number between 1 and 100.
"""
object GuessTheNumberGame:Game {
    can init(attempts: int = 10) {
        <super>.init(attempts);
        <self>.correct_number = random.randint(1, 100);
    }

    can play() {
        while self.attempts > 0 {
            guess = input("Guess a number between 1 and 100: ");
            if guess.isdigit() {
                <self>.process_guess(int(guess));
            } else {
                print("That's not a valid number! Try again.");
            }
        }

        print("Sorry, you didn't guess the number. Better luck next time!");
    }

    can process_guess(guess: int) {
        if guess > self.correct_number {
            print("Too high!");
        } elif guess < self.correct_number {
            print("Too low!");
        } else {
            print("Congratulations! You guessed correctly.");
            self.attempts = 0;  // end the game
        }

        self.attempts -= 1;
        print(f"You have {self.attempts} attempts left.");
    }
}

# Run the game
with entry {
    game = GuessTheNumberGame();
    game.play();
}
```