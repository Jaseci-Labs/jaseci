"""A Number Guessing Game"""

import random;


obj Game {
    def init(attempts: int) {
        self.attempts = attempts;
        self.won = False;
    }
    
    def play() {
        raise NotImplementedError("Subclasses must implement this method.") ;
    }
}


obj GuessTheNumberGame (Game) {
    def init(attempts: int = 10) {
        super.init(attempts);
        self.correct_number = random.randint(1, 100);
    }
    
    def play() {
        while self.attempts > 0 {
            guess = input("Guess a number between 1 and 100: ");
            if guess.isdigit() {
                self.process_guess(int(guess));
            } else {
                print("That's not a valid number! Try again.");
            }
        }
        if not self.won {
            print("Sorry, you didn't guess the number. Better luck next time!");
        }
    }
    
    def process_guess(guess: int) {
        if guess > self.correct_number {
            print("Too high!");
        } elif guess < self.correct_number {
            print("Too low!");
        } else {
            print("Congratulations! You guessed correctly.");
            self.attempts = 0;
            # end the game
            self.won = True;
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
