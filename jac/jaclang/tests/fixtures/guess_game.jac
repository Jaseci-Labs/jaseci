"""A Number Guessing Game"""

import:py random;

glob guesses = [50, 25, 35, 30];

walker GuessGame {
    has correct_number: int = 30;

    can start_game with `root entry;
    can process_guess(guess: int);
}

node turn {
    can check with GuessGame entry;
}

:node:turn:can:check {
    guess = guesses.pop(0);
    guess |> here.process_guess;
    visit [-->];
}

:walker:GuessGame:can:start_game {
    end = here;
    for i=0 to i<10 by i+=1  {
        end ++> (end := :> turn);
    }
    visit [-->];
}

:walker:GuessGame:can:process_guess
(guess: int) {
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
    root spawn GuessGame();
}
