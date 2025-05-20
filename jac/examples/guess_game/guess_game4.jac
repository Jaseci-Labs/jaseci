"""A Number Guessing Game"""
import random;


obj Game {
    has attempts: int, won: bool = False;
    
    def play;
}


obj GuessTheNumberGame (Game) {
    has correct_number: int = (1, 100) |> random.randint;
    
    def init;
    override def play;
    def process_guess(guess: int);
}


impl Game.play {
    raise "Subclasses must implement this method." |> NotImplementedError ;
}


impl GuessTheNumberGame.init {
    self.attempts = 10;
}


impl GuessTheNumberGame.play {
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


impl GuessTheNumberGame.process_guess (guess: int) {
    if guess > self.correct_number {
        "Too high!" |> print;
    } elif guess < self.correct_number {
        "Too low!" |> print;
    } else {
        "Congratulations! You guessed correctly." |> print;
        self.attempts = 0;
        # end the game
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
