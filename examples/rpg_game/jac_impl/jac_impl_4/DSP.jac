walker game{
    has game_started = False;

    can start_game with `<root> entry{
        g = Game();
        game_started = True;
        <here> ++> start_screen;
        visit -->;
        
    };
};

node level{
    has game_level = 1;
    has played = False;
    can run_game with game entry {
        g.new();
        g.main();
        if g.won == True{
            g.game_won();
            <here> ++> level(game_level = game_level+1);
            played = True;
            visit -->;
        } else {
            g.game_over();
            played = True;
            visit <--;
        }

    }
};

node start_screen {
    can intro_screen with game entry {
        if game_started == 
        g.intro_screen();
        <here> ++> level;
        visit -->;
    }

};