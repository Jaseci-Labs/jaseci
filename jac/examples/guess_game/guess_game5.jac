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




# Run the game
 with entry {
    :> GuessGame spawn root;
}
