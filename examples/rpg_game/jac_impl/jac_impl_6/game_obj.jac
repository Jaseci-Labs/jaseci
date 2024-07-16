"""This is an RPG game built using Jaclang"""

# This game is built using the pygame module which is imported here
import:py pygame;

# Including Jac codebase
include:jac sprites;
include:jac settings.config;
include:jac settings.map;

# Including Implementations
include:jac impl.game_obj_impl;

"""
The Game base class
"""
obj Game {
    has screen:pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)),
        clock:pygame.time.Clock = pygame.time.Clock(),
        running:bool = True,
        won:bool = False,
        score:int = 0,
        deaths:int = 0,
        character_spritesheet:pygame.surface.Surface = Spritesheet('../img/character.png'),
        terrain_spritesheet:pygame.surface.Surface = Spritesheet('../img/terrain.png'),
        enemy_spritesheet:pygame.surface.Surface = Spritesheet('../img/enemy.png'),
        attack_spritesheet:pygame.surface.Surface = Spritesheet('../img/attack.png'),
        intro_background:pygame.surface.Surface = pygame.image.load('../img/introbackground.png'),
        go_background:pygame.surface.Surface = pygame.image.load('../img/gameover.png'),
        GameMap:Map = Map();

    can postinit;
    can createTilemap;
    can new;
    can events;
    can update;
    can draw;
    can main;
    can intro_screen;
    can game_won;
    can game_over;

}