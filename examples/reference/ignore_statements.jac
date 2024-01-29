walker GuessGame {
    can start_game with `<root> entry;
}
node turn {
    can check with GuessGame entry;
}

:walker:GuessGame:can:start_game {
    for i=0 to i<10 by i+=1 {
        <here> ++> turn();
    }
    for i=0 to i<5 by i+=1 {
        ignore -->[i];
    }
    visit -->;
}
:node:turn:can:check {
    print("here", end=", ");
}
with entry {
    <root> spawn GuessGame();
}
