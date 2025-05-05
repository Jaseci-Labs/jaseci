"""This is the Data Spatial Implementation of the RPG Game"""


# This game is built using the pygame module which is imported here
import pygame;
import sys;
import random;
import time;

# Importing Jac codebase
import sprites;
import config;
import map;
import game_obj;

'''The walker that initiates the game and runs an instance of the game'''
walker game {
    has g:Game = None,
        current_level:int = 1,
        fwd_dir:bool = True,
        map_directory:dict={};

    can start_game with `root entry;
    can generate_level();
}

edge play{

    has level_id:str = '1_1000';
}

'''Start screen node which operate as the virtual root node'''
node start_screen {
    has game_started: bool = False;

    can intro_screen with game entry;
    can exit_game with game exit;
}

'''Level node which (should) have unique (ai generated) attributes'''
node level{
    has game_level:int = 1,
        level_id:str = '1_1000',
        played:bool = False,
        levelconfig:Map = Map(),
        level_time:float=500000;

    can run_game with game entry;
    can exit_game with game exit;
}

'''Run the game'''
with entry {
    root spawn game();
}
#=Walker=&=Node=Abilities=======================================

:walker:game:can:start_game {
    self.g = Game();
    here ++> start_screen();
    visit [-->];
}

:walker:game:can:generate_level {
    self.map_directory[str(self.current_level)] = Map();
}

:node:level:can:run_game {
    # print("Walker Entry ->", self.level_id);

    if self.played == False {
        if here.current_level != self.game_level {
            here.current_level = self.game_level;
        }
        if str(self.game_level) not in here.map_directory.keys(){
            here.generate_level();
        }

        here.g.GameMap.map = here.map_directory[str(self.game_level)].map;
        here.g.new();
        print(":-: Playing Level :", self.game_level, "| Level ID :",  self.level_id, "| Played :", str(self.played));
        start_time = time.time();
        here.g.main();
        end_time = time.time();
        if here.g.won == True{
            self.level_time = end_time - start_time;
            if self.level_time < here.map_directory[str(self.game_level)].time_to_win_level {
                here.map_directory[str(self.game_level)].time_to_win_level = self.level_time;
            }
            print('Time:', self.level_time);
            here.g.game_won();
            self.played = True;
            here.g.won = False;
            here.fwd_dir =True;
            new_ID = str(self.game_level+1) + "_" + str(random.randint(1000, 9000));
            self +>:play:level_id=new_ID:+> level(game_level = self.game_level+1, level_id = new_ID);
            visit [->:play:level_id==new_ID:->];
        } else {
            here.g.game_over();
            self.played = True;
            here.g.won = False;
            here.fwd_dir = False;
            visit [<-:play:<-];
        }
    } elif here.fwd_dir == False{
        new_ID = str(self.game_level+1) + "_" + str(random.randint(1000, 9000));
        print(":-: Visiting Level :", self.game_level, "| Level ID :",  self.level_id, "| Played :", str(self.played), '| Created Level ID :', new_ID);
        here.fwd_dir = True;
        self +>:play:level_id=new_ID:+> level(game_level = self.game_level+1, level_id = new_ID);
        visit [->:play:level_id==new_ID:->];
    } else {
        print(":-: Visiting Level :", self.game_level, "| Level ID :",  self.level_id, "| Played :", str(self.played));
        visit [<--];
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
        self +>:play:level_id=new_ID:+> level(game_level = 1, level_id = new_ID);
        here.fwd_dir = True;
        visit [->:play:level_id==new_ID:->];
    } else {
        new_ID = str(1) + "_" + str(random.randint(1000, 9000));
        self +>:play:level_id=new_ID:+> level(game_level = 1, level_id = new_ID);
        print(":-: Visiting Intro Screen | Created Level ID :", new_ID);
        here.fwd_dir = True;
        visit [->:play:level_id==new_ID:->];

    }
}

:node:start_screen:can:exit_game {
    if here.g.running == False {
        pygame.quit();
        sys.exit();
        disengage;
    }
}
