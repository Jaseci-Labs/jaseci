import:py from hugchat.login, Login;
import:py from hugchat, hugchat;
include:jac _secrets;

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

obj 'Consists of level configuration data of a certain level'
Map {
    has 'Level number'
    Level_no: int = 1;
    has 'time taken to complete the level in seconds'
    time_to_win_level:float = 60.0;
    has 'the map of the level having B as block, E as enemy, P as player and . as empty space. Size is 20 x 20'
    map: list[str] = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B..................B',
                                'B..................B',
                                'B....BBBB..........B',
                                'B..................B',
                                'B..................B',
                                'B.........P........B',
                                'B..................B',
                                'B....E........E....B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B........B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ];
}

glob SAMPLE_MAPS = {
    'Dummy1': Map(
        Level_no=-1,
        time_to_win_level=3.0,
        map = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B..................B',
                                'B..................B',
                                'B..................B',
                                'B..................B',
                                'B..................B',
                                'B.........P........B',
                                'B..................B',
                                'B....E.............B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B........B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ]),

    'Dummy2': Map(
        Level_no=-2,
        time_to_win_level=5.0,
        map = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B..................B',
                                'B........BBBBB.....B',
                                'B..................B',
                                'B..................B',
                                'B.......B..........B',
                                'B.......B.P........B',
                                'B.......B..........B',
                                'B....E..B..........B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B........B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ]),
    'Dummy3': Map(
        Level_no=-3,
        time_to_win_level=10.0,
        map = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B.......E..........B',
                                'B.......BBBBBB.....B',
                                'B.......B..........B',
                                'B.......B..........B',
                                'B.......B..........B',
                                'B.......B.P........B',
                                'B.......B..........B',
                                'B....E..B..........B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B........B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ]),
    'Dummy4': Map(
        Level_no=-4,
        time_to_win_level=15.0,
        map = [
                                'BBBBBBBBBBBBBBBBBBBB',
                                'B.......E..........B',
                                'B.......BBBBBB.....B',
                                'B.......B..........B',
                                'B.......B..........B',
                                'B.......B..........B',
                                'B.......B.P........B',
                                'B.......B..........B',
                                'B....E..B.......E..B',
                                'B..................B',
                                'B..................B',
                                'B.........B........B',
                                'B.........B...E....B',
                                'B.........B........B',
                                'BBBBBBBBBBBBBBBBBBBB'

                            ])

};


glob LEVEL_NO_smstr = 'Level number';
glob TIME_TO_WIN_LEVEL_smstr = 'time taken to complete the level in seconds';
glob MAP_smstr = 'the map of the level having (B) as block, (E) as enemy, (P) as player and (.) as empty space. Size is 20 x 20. All rows should have 20 characters and there should be 20 rows Where all outer characters are B. Only one single player character can be in the map, placed as far away from other enemy characters. Blocks can be added inside the map to increase map complexity';

obj model {

    has input:dict = {},
        sign:Any = Login(email, passwd),
        cookie_path_dir:str = "./cookies_snapshot",
        cookies:Any = None,
        chatbot:Any = None;

    can <post_init> {
        <self>.cookies = <self>.sign.login();
        <self>.sign.saveCookiesToDir(<self>.cookie_path_dir);

        # start a new huggingchat connection
        <self>.chatbot = hugchat.ChatBot(cookies=<self>.cookies.get_dict());
    }

    can create_prompt(input:dict)->str{
        prompt = '[System Prompt]\nThis is an operation you must perform and return the output values only. Neither, the methodology, extra sentences nor the code are needed.\n';
        prompt += '\n[Information]\n';
        # node_level = <here>;
        level_config_dict:dict = {};
        for config_key in input.keys(){
            level_key = 'Level_' + config_key;
            level_config_dict[level_key] = {};
            # level_config_dict[level_key] = vars(<self>.map_directory[config_key]);
            level_config_dict[level_key]['Level_no'] = ['int', LEVEL_NO_smstr ,input[config_key].Level_no];
            level_config_dict[level_key]['time_to_win_level'] = ['float', TIME_TO_WIN_LEVEL_smstr ,input[config_key].time_to_win_level];
            level_config_dict[level_key]['map'] = ['list[str]', MAP_smstr ,input[config_key].map];
        }

        prompt += 'dict, Map directory that containes all the levels and their configurations of a game where the player is the character controlled by the person playing the game, ' + str(level_config_dict) + '\n';
        prompt += '\n[Output Type]\n';
        prompt += 'List[str]\n';
        prompt += '\n[Output Type Explanation]\n';
        prompt += MAP_smstr + 'The additional Bricks, one more enemy than in the previous level should replace the . on a map like,' + str(['BBBBBBBBBBBBBBBBBBBB','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','B..................B','BBBBBBBBBBBBBBBBBBBB'])+'\n';
        prompt += '\n[Action]\n';
        prompt += 'Return the map of the level which is slightly harder than previous levels which also has the [Output type] and [Output Type Explanation]. Must have one Player (P) in map \n';
        prompt += '\n[Contex]\n';
        prompt += 'The previous level maps are included in [Infomation]. Difficulty can be assesed by the time taken to finish the map. P cam only be at inner positions.\n';
        prompt += '\n[Result] <result>\n';

        return prompt;
    }

    can get_response(prompt:str){

        # start a new conversation
        <self>.chatbot.delete_all_conversations();
        id = <self>.chatbot.new_conversation();
        <self>.chatbot.change_conversation(id);
        <self>.chatbot.switch_llm(0);

        # print the response
        response = <self>.chatbot.chat(prompt);
        return response;
    }

    can generate(input:str){
        prompt = <self>.create_prompt(input);
        response = <self>.get_response(prompt);
        print(response);
    }
}