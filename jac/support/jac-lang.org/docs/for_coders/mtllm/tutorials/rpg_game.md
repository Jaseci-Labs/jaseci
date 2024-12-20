# <span style="color: orange">Creating a Level Generator for an RPG Game

Procedurally generated maps in video games has become a hot topic in the recent years among the gaming community. the algorithms for generating these maps are extremely complected, and requires months of development to build such algorithms. Instead of symbolically written programs, what if we can use generative models to generate these maps?

In this Tutorial we will show you how you can generate game maps for a simple game where the map can be expressed using a list of strings.

## <span style="color: orange">What is a level?

A level can be represented in this hypothetical game using a list of strings shown below.

```jac
glob level = [  'BBBBBBBBBB',
                'B....E...B',
                'B.P......B',
                'B.....B..B',
                'B.....BE.B',
                'B....BBBBB',
                'B....B...B',
                'B.....E..B',
                'BBBBBBBBBB'   ];
```

In this level each character represent a different element in the map,

- 'B'   : Walls
- '.'   : Floor
- 'E'   : Enemy
- 'P'   : Player

## <span style="color: orange">Building a level map generator?

The straightforward approach to build a map generator is to ask from the LLM to directly generate such a map as a list of strings. MTLLM allows you to do this by defining a function or a method. However, here we would discuss a more object oriented way of programming with LLMs which allow the model to 'think' using objects.

### <span style="color: orange">Level Configuration

```jac
obj Level {
    has name: str,
        difficulty: int;
    has width: int,
        height: int,
        num_wall: int,
        num_enemies: int;
    has time_countdown: int,
        n_retries_allowed: int;
}
```

Each level should have a basic configuration which describes the level in an abstract format. This level object embeds the difficulty of the level and the number of enemies and obstacles including other level configuration parameters.

However, filling in the values for fields requires a cognitive capacity, for which will use an LLM later on.

### <span style="color: orange">Building the Map Elements

- <span style="color: orange">**A coordinate system**

```jac
obj Position {
    has x: int,
        y: int;
}
```

As the map we are aiming to generate is a 2D map the position of each object on the map can be designated using the ```Position``` custom type. It is simply representing a cartesian 2D coordinate system.

- <span style="color: orange">**Object to Represent a Wall**

```jac
obj Wall {
    has start_pos: Position,
        end_pos: Position;
}
```

The wall object represents a straight wall, as all obstacles in the 2D map can be represented by a collection of intersecting wall objects. Here each wall object will have a start position as well as a stop position

- <span style="color: orange">**Map represented using objects**

```jac
obj Map {
    has level: Level;
    has walls: list[Wall],
        small_obstacles: list[Position];
    has enemies: list[Position];
    has player_pos: Position;
}
```

This Map object will hold the exact positions of all objects in the map. This is the object that we will generate using MT-LLM. Each field of this object is one of or a derivative of the custom types which we described above.

### <span style="color: orange">The Level Manager

To manage all the generations we can define a Level manager object which can hold a directory of previous levels configurations and maps, which can be used to feed the LLM to give context about the play style of the player. We will be using the OpenAI GPT-4o as the LLM in this tutorial.

```jac
import:py from mtllm.llms, OpenAI;
glob llm = OpenAI(model_name="gpt-4o");

obj LevelManager {
    has current_level: int = 0,
        current_difficulty: int = 1,
        prev_levels: list[Level] = [],
        prev_level_maps: list[Map] = [];

    '''Generates the Next level configuration based upon previous playthroughs'''
    can create_next_level( last_levels: list[Level],
                           difficulty: int,
                           level_width: int,
                           level_height: int) -> Level by llm(temperature=1.0);

    '''Get the Next Level'''
    can get_next_level -> tuple(Level, Map);

    '''Generate the Map as a List of Strings'''
    can get_map(map: Map) -> list[str];
}
```

We have three methods defined under the level manager. Each will handle a separate set of tasks.

- ```create_next_level``` : Takes in previous level configuration data from previously played levels and generate the new level configuration parameters and output a ```Level``` object which describes the new map, using the LLM.

- ```get_next_level``` : Uses the ```create_next_level``` to generate the ```Level``` config. object which is then used to fill in the rest of a newly initiated ```Map``` object using an LLM. This is where the actual map generation happens. Still the generated map cannot be visualize.

- ```get_map``` : This method will generate the actual list of strings which can be used with an actual game using the ```Map``` object generated by ```get_next_level``` method. This does not require any LLM as all objects of the map are included in the ```Map``` object with their exact positions.

The implementation of the above methods are as follows.

```jac
:obj:LevelManager:can:get_next_level {
    self.current_level += 1;
    # Keeping Only the Last 3 Levels
    if len(self.prev_levels) > 3 {
        self.prev_levels.pop(0);
        self.prev_level_maps.pop(0);
    }

    # Generating the New Level
    new_level = self.create_next_level(
        self.prev_levels,
        self.current_difficulty,
        20, 20
    );

    self.prev_levels.append(new_level);
    # Generating the Map of the New Level
    new_level_map = Map(level=new_level by llm());
    self.prev_level_maps.append(new_level_map);
    # Increasing the Difficulty for end of every 2 Levels
    if self.current_level % 2 == 0 {
        self.current_difficulty += 1;
    }

    return (new_level, new_level_map);
}
```

In the ```get_next_level``` method there are two llm calls which we will discuss in this tutorial while other parts are related the functionality of the game.

- ```Line 9-13``` : Here the saved data from previous levels are given as inputs which are defined previously along with the basic level config parameters of the new level. As the output type of this method was specified above to be a ```Level``` object the LLM will initiate and fill in the values of the objects. As the LLM hyperparameter temperature, is set for 1.0 at method declaration, the LLM is forced to be more creative.

- ```Line 14``` : Here the programmer is initiating a Map object while passing in only the level parameter with the newly generated ```level``` object and ask the LLM to fill in the rest of the fields by generating the relevant types. This nested type approach ensures the output is formatted according to how you expect them to be.

```jac
:obj:LevelManager:can:get_map {
    map_tiles = [['.' for _ in range(map.level.width)] for _ in range(map.level.height)];
    for wall in map.walls {
        for x in range(wall.start_pos.x, wall.end_pos.x + 1) {
            for y in range(wall.start_pos.y, wall.end_pos.y + 1) {
                map_tiles[y-1][x-1] = 'B';
            }
        }
    }

    for obs in map.small_obstacles {
        map_tiles[obs.y-1][obs.x-1] = 'B';
    }

    for enemy in map.enemies {
        map_tiles[enemy.y-1][enemy.x-1] = 'E';
    }
    map_tiles[map.player_pos.y-1][map.player_pos.x-1] = 'P';
    map_tiles = [['B'] + row + ['B'] for row in map_tiles];
    map_tiles = [['B' for _ in range(map.level.width + 2)]] + map_tiles + [['B' for _ in range(map.level.width + 2)]];
    return [''.join(row) for row in map_tiles];
}
```

### <span style="color: orange">Running the Program

```jac
with entry {
    level_manager = LevelManager();
    for _ in range(2) {
        (new_level, new_level_map) = level_manager.get_next_level();
        print(new_level);
        print('\n'.join(LevelManager.get_map(new_level_map)));
    }
}
```

This program will now generate two consecutive maps and print them on the terminal. by running this jac file using ```jac run level_manager.jac``` you can simply test your program.

## <span style="color: orange">A full scale game demo

For the sake of this tutorial we have not included the entire development of an actual game. The full game is available on our [jac-lang repo](https://github.com/Jaseci-Labs/jaclang/tree/main/examples/rpg_game). A sample demonstration of the game can be viewed below.

[Demo Video](https://drive.google.com/file/d/1JXyWbmI6vJsjpNUnscRxdnK5vmo8312r/view?usp=sharing)