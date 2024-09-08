"""A Number Guessing Game"""

import:py random;

"""
A generic Game base class.

The obj keyword is used to define the class.
The can keyword is used to define methods (functions) within the class.
The self keyword is used to refer to the current instance of the class.
Constructors are defined using the init method with parameters.
"""
obj Game {
    can init(attempts: int) {
        self.attempts = attempts;
        self.won = False;
    }

    can play() {
        raise NotImplementedError(
            "Subclasses must implement this method."
        );
    }
}

"""
A number guessing game. The player must guess a number between 1 and 100.

This class inherits from Game. The super() function is used to call the parent class constructor.
"""
obj GuessTheNumberGame :Game: {
    can init(attempts: int=10) {
        super.init(attempts);
        self.correct_number = random.randint(1, 100);
    }

    can play() {

        while self.attempts > 0 {
            guess = input("Guess a number between 1 and 100: ");
            if guess.isdigit() {
                self.process_guess(int(guess));
            } else {
                print("That's not a valid number! Try again.");
            }
        }
        if not self.won {
            print(
                "Sorry, you didn't guess the number. Better luck next time!"
            );
        }
    }

    can process_guess(guess: int) {
        if guess > self.correct_number {
            print("Too high!");
        } elif guess < self.correct_number {
            print("Too low!");
        } else {
            print("Congratulations! You guessed correctly.");
            self.attempts = 0;# end the game
            self.won = True;
        }
        self.attempts -= 1;
        print(f"You have {self.attempts} attempts left.");
    }
}
# Run the game

"""
Object instantiation and method invocation occur within the with entry { ... } block.
"""
with entry {
    game = GuessTheNumberGame();
    game.play();
}
