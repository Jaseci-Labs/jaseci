:node:level:can:run_game {
    # print("Walker Entry ->", self.level_id);

    if self.played == False {
        if here.current_level != self.game_level {
            here.current_level = self.game_level;
        }
        if here.manager.current_level != self.game_level {
            if self.game_level != 1 {
                here.manager.current_level = self.game_level;
                next_level = here.manager.get_next_level(self.game_level);
                self.level_config.map = next_level;
            }
        } else {
            self.level_config.map = [[<--][0] -->](`?level)(?level_id==here.last_level_id)[0].level_config.map;
        }
        here.g.GameMap.map = self.level_config.map;
        here.g.new();
        print(":-: Playing Level :", self.game_level, "| Level ID :",  self.level_id, "| Played :", str(self.played));
        start_time = time.time();
        here.g.main();
        end_time = time.time();
        here.last_level_id = self.level_id;
        if here.g.won == True{
            self.level_time = end_time - start_time;
            if here.manager.prev_levels {
                here.manager.prev_levels[-1].time = self.level_time;
            }
            here.g.game_won();
            self.played = True;
            here.g.won = False;
            here.fwd_dir =True;
            new_ID = str(self.game_level+1) + "_" + str(random.randint(1000, 9000));
            self +>:play:level_id=new_ID:+> level(game_level = self.game_level+1, level_id = new_ID);
            visit [->:play:level_id==new_ID:->];
        } else {
            here.g.game_over();
            # here.map_directory[str(self.game_level)].nos_retry += 1;
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