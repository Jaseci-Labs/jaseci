glob WIN_WIDTH = 640;
glob WIN_HEIGHT = 480;
glob TILESIZE = 32;
glob FPS = 60;

glob ATTACK_LAYER = 5;
glob ENEMY_LAYER = 4;
glob PLAYER_LAYER = 3;
glob BLOCK_LAYER = 2;
glob GROUND_LAYER = 1;

glob PLAYER_SPEED = 3;
glob ENEMY_SPEED = 2;

glob RED = (255, 0, 0);
glob BLACK = (0, 0, 0);
glob BLUE = (0, 0, 255);
glob WHITE = (255, 255, 255);

glob GENERAL_FONT = '../fonts/8bitoperator_jve.ttf';

obj Map {
    has Level_no: int = 1,
        time_to_win_level:float = 60.0,
        map: list[str] = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B..E...............B',
                                'B..................B',
                                'B....BBBB......E...B',
                                'B..................B',
                                'B..................B',
                                'B.........P........B',
                                'B..................B',
                                'B....E.............B',
                                'B..................B',
                                'B.......BBB........B',
                                'B.........B........B',
                                'B.........B....E...B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ];
}