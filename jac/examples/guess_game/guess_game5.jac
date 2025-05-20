"""A Number Guessing Game"""

import random;


walker GuessGame {
    has correct_number: int = (1, 100) |> random.randint;
    
    can start_game with `root entry;
    def process_guess(guess: int);
}


node turn {
    can check with GuessGame entry;
}


impl turn.check {
    guess = "Guess a number between 1 and 100: " |> input;
    if |> guess.isdigit {
        guess |> int |> here.process_guess;
    } else {
        "That's not a valid number! Try again." |> print;
    }
    visit [-->];
}


impl GuessGame.start_game {
    end : `root | turn = here;
    for i = 0 to i < 10 by i += 1 {
        end ++> (end := turn());
    }
    visit [-->];
}


impl GuessGame.process_guess (guess: int) {
    if guess > self.correct_number {
        "Too high!" |> print;
    } elif guess < self.correct_number {
        "Too low!" |> print;
    } else {
        "Congratulations! You guessed correctly." |> print;
        disengage;
    }
}


# Run the game
 with entry {
    :> GuessGame spawn root;
}
