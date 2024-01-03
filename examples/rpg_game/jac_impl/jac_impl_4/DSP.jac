# This game is built using the pygame module which is imported here
import:py pygame;
import:py sys;

# Importing Jac codebase
include:jac sprites;
include:jac config;
include:jac map;
include:jac main;

'''The walker that initiates the game and runs an instance of the game'''
walker game{

    has g:Game = None;
    can start_game with `<root> entry;
}

'''Start screen node which operate as the virtual root node'''
node start_screen {
    
    has game_started:bool = False;

    can intro_screen with game entry;
    can exit_game with game exit;

}

'''Level node which (should) have unique (ai generated) attributes'''
node level{
    has game_level:int = 1,
        played:bool = False;

    can run_game with game entry;
    can exit_game with game exit;
}

'''Run the game'''
with entry {
    game() spawn <root>;
}

#=Walker=&=Node=Abilities=======================================

:walker:game:can:start_game {
    <self>.g = Game();
    <here> ++> start_screen();
    visit -->;
}
:node:level:can:run_game {
    <here>.g.new();
    <here>.g.main();
    if <here>.g.won == True{
        <here>.g.game_won();
        <self> ++> level(game_level = <self>.game_level+1);
        <self>.played = True;
        visit -->;
    } else {
        <here>.g.game_over();
        <self>.played = True;
        visit <--;
    }
}
:node:level:can:exit_game {
    if <here>.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    } 
}
:node:start_screen:can:intro_screen {
    if <self>.game_started == False {
        <self>.game_started = True;
        <here>.g.intro_screen();
        <self> ++> level();
        visit -->;
    } else {
        <self> ++> level();
        visit -->;
    } 
}
:node:start_screen:can:exit_game {
    if <here>.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    } 
}

