"""A Number Guessing Game"""

import random;

"""
A generic Game base class.

Inside the Game class, we define a can play method that raises a NotImplementedError.
This is way in jaclang to define abstract methods in base classes that must be implemented by subclasses.
In this case it ensure that any subclass of Game must implement a play method.
"""
obj Game {
    has attempts: int,
        won: bool = False;

    def play;
}

"""
A number guessing game. The player must guess a number between 1 and 100.

"""
obj GuessTheNumberGame(Game) {
    has correct_number: int = (1, 100) |> random.randint;

    def init;
    override def play;
    def process_guess(guess: int);
}

"""
The init method sets the number of attempts to 10.
:ob:Game:can:play method is implemented to run the game. This another way in jaclang to add methods to a existing class.
"""
:obj:Game:can:play {
    raise "Subclasses must implement this method." |> NotImplementedError;
}

:obj:GuessTheNumberGame:can:init {
    self.attempts = 10;
}

:obj:GuessTheNumberGame:can:play {
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

:obj:GuessTheNumberGame:can:process_guess
(guess: int) {
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
# Run the game

with entry {
    game = |> GuessTheNumberGame;
    |> game.play;
}
