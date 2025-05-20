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




# Run the game
 with entry {
    game = |> GuessTheNumberGame;
    |> game.play;
}
