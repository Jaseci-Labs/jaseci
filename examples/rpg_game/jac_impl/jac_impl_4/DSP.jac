"""This is the Data Spatial Implementation of the RPG Game"""


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
walker game {
    has g: Game = None,
        fwd_dir: bool = True;

    can start_game with `root entry;
}

'''Start screen node which operate as the virtual root node'''
node start_screen {
    has game_started: bool = False;

    can intro_screen with game entry;
    can exit_game with game exit;
}

'''Level node which (should) have unique (ai generated) attributes'''
node level {
    has game_level: int = 1,
        level_id: str = '1_1000',
        played: bool = False,
        levelmap: list[str] = Map();

    can run_game with game entry;
    can exit_game with game exit;
}

'''Run the game'''
with entry {
    game() spawn root;
}
#=Walker=&=Node=Abilities=======================================

:walker:game:can:start_game {
    self.g = Game();
    here ++> start_screen();
    visit [-->];
}

:node:level:can:run_game {
# print("Walker Entry ->", self.level_id);
if self.played == False {
    here.g.GameMap.map = self.levelmap.map;
    here.g.new();
    print(":-: Playing Level :", self.game_level, "| Level ID :", self.level_id, "| Played :", str(self.played));
    here.g.main();
    if here.g.won == True {
        here.g.game_won();
        self.played = True;
        here.g.won = False;
        here.fwd_dir = True;
        new_ID = str(self.game_level + 1) + "_" + str(random.randint(1000, 9000));
        self ++> level(game_level=self.game_level + 1, level_id=new_ID);
        visit [-->];
    } else {
        here.g.game_over();
        self.played = True;
        here.g.won = False;
        here.fwd_dir = False;
        visit [<--];
    }
} elif here.fwd_dir == False {
    new_ID = str(self.game_level + 1) + "_" + str(random.randint(1000, 9000));
    print(":-: Visiting Level :", self.game_level, "| Level ID :", self.level_id, "| Played :", str(self.played), '| Created Level ID :', new_ID);
    here.fwd_dir = True;
    self ++> level(game_level=self.game_level + 1, level_id=new_ID);
    visit [-->];
}
}

:node:level:can:exit_game {
    if here.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    }
}

:node:start_screen:can:intro_screen {
# print("Walker Entry -> Intro Screen");
if self.game_started == False {
    self.game_started = True;
    here.g.intro_screen();
    new_ID = str(1) + "_" + str(random.randint(1000, 9000));
    self ++> level(game_level=1, level_id=new_ID);
    here.fwd_dir = True;
    visit [-->];
} else {
    new_ID = str(1) + "_" + str(random.randint(1000, 9000));
    self ++> level(game_level=1, level_id=new_ID);
    print(":-: Visiting Intro Screen | Created Level ID :", new_ID);
    here.fwd_dir = True;
    visit [-->];
}
}

:node:start_screen:can:exit_game {
    if here.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    }
}
