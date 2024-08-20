import:py from mtllm.llms.base { BaseLLM }
import:py json;
import:py os;
import:py random;

glob output_str = "None";

obj model :BaseLLM: {
    can init {
        self.verbose = True;
        self.max_tries = 1;
    }

    can __infer__(meaning_in: str, **kwargs: dict) {
        :g: output_str ;

        return f"[Output] {output_str}";
    }
}

glob llm = model();

obj Position {
    has x: int,
        y: int;
}

obj Wall {
    has start_pos: Position,
        end_pos: Position;
}

obj Map {
    has level: Level;
    has walls: list[Wall],
        small_obstacles: list[Position];
    has enemies: list[Position];
    has player_pos: Position;
}

obj Level {
    has name: 'Fantasy based Name': str,
        difficulty: int;
    has width: int,
        height: int,
        num_wall: int,
        num_enemies: int;
    has time_countdown: int,
        n_retries_allowed: int;
}

obj LevelManager {
    has current_level: int = 0,
        current_difficulty: int = 1,
        prev_levels: list[Level] = [],
        prev_level_maps: list[Map] = [];

    can create_next_level(last_levels: list[Level], difficulty: int, level_width: int, level_height: int) -> Level by llm(temperature=1.0);
    '''Get the Next Level'''
    can get_next_level -> tuple(Level, Map) {
        :g: output_str ;

        self.current_level += 1;

        # Keeping Only the Last 2 Levels
        if len(self.prev_levels) > 2 {
            self.prev_levels.pop(0);
            self.prev_level_maps.pop(0);
        }
        # Generating the New Level
        output_str = str(
            Level(
                name="Level_" + str(self.current_level),
                difficulty=self.current_difficulty,
                width=random.randint(10, 30 + self.current_difficulty * 5),
                height=random.randint(10, 30 + self.current_difficulty * 5),
                num_wall=random.randint(10, 20 + self.current_difficulty * 5),
                num_enemies=random.randint(5, 10 + self.current_difficulty * 2),
                time_countdown=random.randint(100, 300 + self.current_difficulty * 50),
                n_retries_allowed=random.randint(1, 5 + self.current_difficulty)
            )
        );
        new_level = self.create_next_level(
            self.prev_levels,
            self.current_difficulty,
            20,
            20
        );
        self.prev_levels.append(new_level);
        # Generating the Map of the New Level
        output_str = str(
            Map(
                level=new_level,
                walls=[Wall(
                    start_pos=Position(
                        x=random.randint(1, new_level.width),
                        y=random.randint(1, new_level.height)
                    ),
                    end_pos=Position(
                        x=random.randint(1, new_level.width),
                        y=random.randint(1, new_level.height)
                    )
                ) for _ in range(new_level.num_wall)],
                small_obstacles=[Position(
                    x=random.randint(1, new_level.width),
                    y=random.randint(1, new_level.height)
                ) for _ in range(5)],
                enemies=[Position(
                    x=random.randint(1, new_level.width),
                    y=random.randint(1, new_level.height)
                ) for _ in range(new_level.num_enemies)],
                player_pos=Position(
                    x=random.randint(1, new_level.width),
                    y=random.randint(1, new_level.height)
                )
            )
        );
        new_level_map = Map(level=new_level by llm());
        self.prev_level_maps.append(new_level_map);
        # Increasing the Difficulty for end of every 2 Levels
        if self.current_level % 2 == 0 {
            self.current_difficulty += 1;
        }
        return (new_level, new_level_map);
    }
}

'''Get the map of the level'''
can get_map(map: Map) -> str {
    map_tiles = [['.' for _ in range(map.level.width)] for _ in range(map.level.height)];

    for wall in map.walls {
        for x in range(wall.start_pos.x, wall.end_pos.x + 1) {
            for y in range(wall.start_pos.y, wall.end_pos.y + 1) {
                map_tiles[y - 1][x - 1] = 'B';
            }
        }
    }

    for obs in map.small_obstacles {
        map_tiles[obs.y - 1][obs.x - 1] = 'B';
    }

    for enemy in map.enemies {
        map_tiles[enemy.y - 1][enemy.x - 1] = 'E';
    }
    map_tiles[map.player_pos.y - 1][map.player_pos.x - 1] = 'P';
    map_tiles = [['B'] + row + ['B'] for row in map_tiles];
    map_tiles = [['B' for _ in range(map.level.width
        + 2)]]
        + map_tiles
        + [['B' for _ in range(map.level.width
        + 2)]];
    return [''.join(row) for row in map_tiles];
}

with entry {
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "program_args.json"
        ),
        "r"
    ) as f {
        args = json.load(f);
    }
    current_level = args["current_level"];
    level_difficulty = args["level_difficulty"];
    level_manager = LevelManager(current_level, level_difficulty);
    for _ in range(3) {
        (new_level, new_level_map) = level_manager.get_next_level();
    }
}
