import:py from openai, ChatCompletion;
import:py openai;
import:py re;
import:py ast;

# include:jac _secrets;

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
    has Level_no:'Level number':int = 1;
    has time_to_win_level:'time taken to complete the level in seconds':float = 60.0;
    has map:
    'the map of the level having (B) as block, (E) as enemy, (P) as player and (.) as empty space.All outer characters are B. Only one single player character can be in the map.'
    :list[str] = [
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


glob LEVEL_NO_smstr = 'Level number';
glob TIME_TO_WIN_LEVEL_smstr = 'time taken to complete the level in seconds';
glob MAP_smstr = 'the map of the level having (B) as block, (E) as enemy, (P) as player and (.) as empty space.All outer characters are B. Only one single player character can be in the map.';

obj model {

    has input:dict = {};

    can create_prompt(input:dict)->str{
        level_config_dict:dict = {};
        for config_key in input.keys(){
            level_key = 'Level_' + config_key;
            level_config_dict[level_key] = {};
            # level_config_dict[level_key] = vars(self.map_directory[config_key]);
            level_config_dict[level_key]['Level_no'] = ['int', LEVEL_NO_smstr ,input[config_key].Level_no];
            level_config_dict[level_key]['time_to_win_level'] = ['float', TIME_TO_WIN_LEVEL_smstr ,input[config_key].time_to_win_level];
            level_config_dict[level_key]['map'] = ['list[str]', MAP_smstr ,input[config_key].map];
        }

        prompt = ""
        "[System Prompt]"
        "This is an operation you must perform and return the output values only. Neither, the methodology, extra sentences nor the code are needed."

        "[Information]"
        f"Map_directory, dict, Map directory that containes all the levels and their configurations of a game where the player is the character controlled by the person playing the game,  {str(level_config_dict)} "

        "[Output Type]"
        "List[str]"

        "[Output Type Explanation]"
        f"{MAP_smstr}"

        "[Prompt]"
        "Return the map of the next level which is different and incrementally challenging than previous levels."

        "[Context]"
        "Must have one Player (P) in map."
        "Two consecutive maps should not look alike."
        "Hardness should be slightly increased."
        "All enemies should be accessible to the player (should not be enclosed with blocks)."
        "The previous level maps are included in [Infomation]. Difficulty can be assesed by the time taken to finish the map."
        "Blocks can be added inside the map to increase map complexity."

        "[Result] <result>";

        return prompt;
    }

    can get_response(prompt:str){

        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75
        ).choices[0].message.content;
    }

    can parse_response(response:str)->list[str]{
        # lines = re.findall(r"'([^']*)'", response);
        map = ast.literal_eval(response);
        return map;
    }

    can generate(input:str){
        prompt = self.create_prompt(input);
        response = self.get_response(prompt);
        map = self.parse_response(response);
        return map;
    }
}