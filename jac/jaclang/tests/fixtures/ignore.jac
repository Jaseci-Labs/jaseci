"""Testing ignore."""

walker GuessGame {
    can start_game with `root entry;
}

walker GuessGame2 {
    can start_game with `root entry;
}

node turn {
    can check with GuessGame|GuessGame2 entry;
}


:walker:GuessGame:can:start_game {
    for i=0 to i<10 by i+=1 {
        here ++> turn();
    }
    visit [-->];
}

:walker:GuessGame2:can:start_game {
    for i=0 to i<10 by i+=1 {
        here ++> turn();
    }
    for i=0 to i<15 by i+=1 {
        ignore [-->][i];
    }
    visit [-->];
}

:node:turn:can:check {
    print("here", end=", ");
}

# # Run the game
with entry {
    root spawn GuessGame();
    print('');
    root spawn GuessGame2();
    print('');
}
