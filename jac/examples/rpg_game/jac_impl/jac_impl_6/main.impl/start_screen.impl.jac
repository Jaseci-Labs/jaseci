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