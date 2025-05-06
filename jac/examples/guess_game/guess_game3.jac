"""A Number Guessing Game"""

import random;

"""
A generic Game base class.

In the following code |> is pipe forward operator, it assigns the lefthand side values
as arguments of the right hand side function.
i.e, "Hello" |> print is equivalent to print("Hello")
"""
obj Game {
    has attempts: int,
        won: bool = False;

    def play {
        raise "Subclasses must implement this method." |> NotImplementedError;
    }
}

"""
A number guessing game. The player must guess a number between 1 and 100.
"""
obj GuessTheNumberGame(Game) {
    has attempts: int = 10,
        correct_number: int = (1, 100) |> random.randint;

    override def play {

        while self.attempts > 0 {
            guess = "Guess a number between 1 and 100: " |> input;
            if |> guess.isdigit {
                guess |> int |> self.process_guess;
            } else {
                "That's not a valid number! Try again." |> print;
            }
        }
        if not self.won {
            "Sorry, you didn't guess the number. Better luck next time!" |> print;
        }
    }

    def process_guess(guess: int) {
        if guess > self.correct_number {
            "Too high!" |> print;
        } elif guess < self.correct_number {
            "Too low!" |> print;
        } else {
            "Congratulations! You guessed correctly." |> print;
            self.attempts = 0;# end the game
            self.won = True;
        }
        self.attempts -= 1;
        f"You have {self.attempts} attempts left." |> print;
    }
}
# Run the game

with entry {
    game = |> GuessTheNumberGame;
    |> game.play;
}
