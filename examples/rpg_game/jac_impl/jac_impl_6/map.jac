obj 'Consists of level configuration data of a certain level'
Map {
    has Level_no:'Level number':int = 1;
    has time_to_win_level:'time taken to complete the level in seconds':float = 60.0;
    has nos_retry:'How many retry attempts before completing the level':int = 0;
    has map:
    'the map of the level having (B) as block, (E) as enemy, (P) as player and (.) as empty space. All outer characters are B. Only one single player character (P) can be in the map.'
    :list[str] = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B...E..............B',
                                'B.......B..........B',
                                'B....BBBB..........B',
                                'B..................B',
                                'B..................B',
                                'B.........P........B',
                                'B..................B',
                                'B.............E....B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B........B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ];
}