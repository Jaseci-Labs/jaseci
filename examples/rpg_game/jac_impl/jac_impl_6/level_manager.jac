import:py from jaclang.core.llms, OpenAI;

glob llm = OpenAI(model_name="gpt-4o");

obj 'Position (0-Indexed)'
Position {
    has x: 'X Coordinate': int,
        y: 'Y Coordinate': int;
}

obj 'Wall'
Wall {
    has start_pos: 'Start Position of the Wall': Position,
        end_pos: 'End Position of the Wall': Position;
}

obj 'Map of the Level'
Abs_Map {
    has level: 'Level of the Map': Level;
    has walls: 'Walls in the Map Other than Edges': list[Wall],
        small_obstacles: 'Obstacles in the Map': list[Position];
    has enemies: 'Enemies in the Map': list[Position];
    has player_pos: 'Player Position in the Map': Position;
}

obj 'Game Level'
Level {
    has name: 'Number of the Level': int,
        difficulty: 'Difficulty of the Level': int,
        time: 'Time to Complete the Level': int;
    has width: 'Width of the Map': int,
        height: 'Height of the Map': int,
        num_wall: 'Number of Walls in the Map': int,
        num_enemies: 'Number of Enemies in the Map': int;
}

obj LevelManager {
    has current_level: int = 1,
        current_difficulty: int = 1,
        prev_levels: list[Level] = [],
        prev_level_maps: list[Abs_Map] = [];

    can 'Create the Next Level'
    create_next_level(last_levels: 'Last Played Levels': list[Level], difficulty: 'Difficulty of the New Level': int) -> 'Next Level': Level by llm(
        temperature=1.0,
        context=["Use the Input Difficulty as the Level Difficulty."
            "Make Sure the New Level is Different from the Previous Levels."
            "Increase of Decrease the Number of Wall, Enemies, Width, Height of the Map according to the Difficulty."
            "Increase or Decrease the Time Countdown and Number of Retries Allowed according to the Difficulty."]
    );
    '''Get the Next Level'''
    can get_next_level (current_level: int) -> tuple(Level, Abs_Map) {

        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3 {
            self.prev_levels.pop(0);
            self.prev_level_maps.pop(0);
        }
        # Generating the New Level
        new_level = self.create_next_level(
            self.prev_levels,
            self.current_difficulty
        );
        self.prev_levels.append(new_level);

        # Generating the Map of the New Level
        new_level_map = Abs_Map(level=new_level by llm(
            context=["Make Sure the Player is not Stuck in the Map."
                "Make Sure the Player can Reach the Enemies."
                "Make Sure Player and Enemies are not in the Same Position and not in the Wall."
                "Make Sure the Player is not really close to the Enemies."
                "Make Sure the Number of Walls and Enemies are Mentioned in the Level is followed."
                "Make Sure the Walls are not placed in the Edges of the Map."]
        ));
        self.prev_level_maps.append(new_level_map);

        # Increasing the Difficulty for end of every 2 Levels
        if self.current_level % 2 == 0 {
            self.current_difficulty += 1;
        }

        new_map = self.get_map(new_level_map);
        return new_map;
    }

    '''Get the map of the level'''
    can get_map(map: Abs_Map) -> str {
        map_tiles = [['.' for _ in range(map.level.width)] for _ in range(map.level.height)];

        for wall in map.walls {
            for x in range(wall.start_pos.x, wall.end_pos.x + 1) {
                for y in range(wall.start_pos.y, wall.end_pos.y + 1) {
                    map_tiles[y][x] = 'B';
                }
            }
        }

        for obs in map.small_obstacles {
            map_tiles[obs.y][obs.x] = 'B';
        }

        for enemy in map.enemies {
            map_tiles[enemy.y][enemy.x] = 'E';
        }
        map_tiles[map.player_pos.y][map.player_pos.x] = 'P';
        map_tiles = [['B'] + row + ['B'] for row in map_tiles];
        map_tiles = [['B' for _ in range(map.level.width + 2)]] + map_tiles + [['B' for _ in range(map.level.width + 2)]];
        return [''.join(row) for row in map_tiles];
    }

}