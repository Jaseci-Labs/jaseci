# This game is built using the pygame module which is imported here
import:py pygame;
import:py sys;
import:py random;

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
        level_id:str = '1_1000',
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
    if <self>.played == False {
  
        <here>.g.new();
        print(":-: Playing Level :", <self>.game_level, "| Level ID :",  <self>.level_id, "| Played :", str(<self>.played));
        <here>.g.main();
        
        if <here>.g.won == True{
            <here>.g.game_won();
            # print('Attach');
            <self>.played = True;
            <here>.g.won = False;
            visit(level(game_level = <self>.game_level+1, level_id = str(<self>.game_level+1) + "_" + str(random.randint(1000, 9000))));
        } else {
            <here>.g.game_over();
            <self>.played = True;
            <here>.g.won = False;
            visit <--;
        }
    } else {
        print(":-: Visiting Level :", <self>.game_level, "| Level ID :",  <self>.level_id, "| Played :", str(<self>.played));
        visit(level(game_level = <self>.game_level+1, level_id = str(<self>.game_level+1) + "_" + str(random.randint(1000, 9000))));
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
        <self> ++> level(game_level = 1, level_id = str(1) + "_" + str(random.randint(1000, 9000)));
        visit -->;
    } else {
        visit(level(game_level = 1, level_id = str(1) + "_" + str(random.randint(1000, 9000))));
        print(":-: Visiting Into Screen | ");
    }
}
:node:start_screen:can:exit_game {
    if <here>.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    }
}