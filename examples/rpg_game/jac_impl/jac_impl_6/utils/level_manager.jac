import:py from mtllm.llms, OpenAI;
include:jac level_manager_impl;

glob llm = OpenAI(model_name="gpt-4o");

obj Position {
    has x: int,
        y: int;
}

obj Wall {
    has start_pos: Position,
        end_pos: Position;
}

obj Map_tiles {
    has level: Level;
    has walls: list[Wall],
        small_obstacles: list[Position];
    has enemies: list[Position];
    has player_pos: Position;
}

obj Level {
    has name: int,
        difficulty: int,
        time: int;
    has width: int,
        height: int,
        num_wall: int,
        num_enemies: int;
}

obj LevelManager {
    has current_level: int = 0,
        current_difficulty: int = 1,
        prev_levels: list[Level] = [],
        prev_level_maps: list[Map_tiles] = [];

    can create_next_level(last_levels: list[Level], difficulty: int)
    -> Level by llm(temperature=0.8);

    '''Get the Next Level'''
    can get_next_level (current_level: int) -> tuple(Level, Map_tiles);

    '''Get the map of the level'''
    can get_map(map: Map_tiles) -> str;

}