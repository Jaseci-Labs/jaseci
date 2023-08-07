"""A Number Guessing Game"""
import:py random;


node turn {
    can check with GuessGame entry;
}

walker GuessGame {
    has correct_number: int = (1, 100) |> random.randint;
    can start_game with <root> entry;
    can process_guess(guess: int);
}

:node:turn:ability:check {
    guess = "Guess a number between 1 and 100: " |> input;
    if |> guess.isdigit {
        guess |> int |> <here>.process_guess;
    } else {
        "That's not a valid number! Try again." |> print;
    }
}

:walker:GuessGame:ability:start_game {
    a = <here> ++> turn;
    for i=0 to i<10 by i+=1 {
        a = a ++> turn;
    }
    visit -->;
}

:walker:GuessGame:ability:process_guess(guess: int) {
    if guess > <self>.correct_number {
        "Too high!" |> print;
    } elif guess < <self>.correct_number {
        "Too low!" |> print;
    } else {
        "Congratulations! You guessed correctly." |> print;
        disengage;
    }
}

# # Run the game
with entry {
    |> GuessGame |> <root>;
}



# """
# A generic Game base class.
# """
# object Game {
#     has attempts: int,
#         won: bool = False;

#     can play;
# }

# """
# A number guessing game. The player must guess a number between 1 and 100.
# """
# object GuessTheNumberGame:Game {
#     has attempts: int = 10,
#         correct_number: int = (1, 100) |> random.randint;

#     can play;
#     can process_guess(guess: int);
# }


# :object:Game:ability:play {
#     raise "Subclasses must implement this method." |> NotImplementedError;
# }

# :object:GuessTheNumberGame:ability:play {
#     while self.attempts > 0 {
#         guess = "Guess a number between 1 and 100: " |> input;
#         if |> guess.isdigit {
#             guess |> int |> <self>.process_guess;
#         } else {
#             "That's not a valid number! Try again." |> print;
#         }
#     }

#     if not <self>.won {
#         "Sorry, you didn't guess the number. Better luck next time!" |> print;
#     }
# }

# :object:GuessTheNumberGame:ability:process_guess(guess: int) {
#     if guess > <self>.correct_number {
#         "Too high!" |> print;
#     } elif guess < <self>.correct_number {
#         "Too low!" |> print;
#     } else {
#         "Congratulations! You guessed correctly." |> print;
#         <self>.attempts = 0;  # end the game
#         <self>.won = True;
#     }

#     <self>.attempts -= 1;
#     f"You have {<self>.attempts} attempts left." |> print;
# }

# # Run the game
# with entry {
#     game = |> GuessTheNumberGame;
#     |> game.play;
# }
