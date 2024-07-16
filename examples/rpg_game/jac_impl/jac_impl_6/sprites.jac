"""This file containes all definitions of sprites that apear in the game"""

# Importing python libraries
import:py pygame, random, math;
import:py from pygame.sprite, AbstractGroup;

# Importing settings data
include:jac settings.config;
include:jac settings.map;

# Including Implementations
include:jac impl.sprites_impl;

"""
Object for impoting sprite character images.
"""
obj Spritesheet {
    has file:str;

    can postinit;
    can get_sprite(x: int, y: int, width: int, height: int) -> pygame.Surface;
}

"""
Object for the player with type pygame.sprite.Sprite
"""
obj Player :pygame.sprite.Sprite: {
    has game: Game,
        x: int,
        y: int;
    has _layer: int = PLAYER_LAYER,
        width: int = TILESIZE,
        height: int = TILESIZE,
        x_change: int = 0,
        y_change: int = 0,
        facing: str = 'down',
        animation_loop: float = 1;

    can postinit;
    can update;
    can movement;
    can collide_enemy;
    can animate;
    can collide_blocks(direction: str);
}

"""
Object for enemies with type pygame.sprite.Sprite
"""
obj Enemy :pygame.sprite.Sprite: {
    has game: Game,
        x: int,
        y: int;
    has _layer: int = ENEMY_LAYER,
        width: inr = TILESIZE,
        height: int = TILESIZE,
        x_change: int = 0,
        y_change: int = 0,
        animation_loop: float = 0,
        movement_loop: int = 0;

    can postinit;
    can update;
    can movement;
    can animate;
    can collide_blocks(direction: str);
}

"""
Object for blocks (Walls) with type pygame.sprite.Sprite
"""
obj Block :pygame.sprite.Sprite: {
    has game: Game,
        x: int,
        y: int;
    has _layer: int = BLOCK_LAYER,
        width: int = TILESIZE,
        height: int = TILESIZE;

    can postinit;
}

"""
Object for ground with type pygame.sprite.Sprite
"""
obj Ground :pygame.sprite.Sprite: {
    has game: Game,
        x: int,
        y: int;
    has _layer: int = GROUND_LAYER,
        width: int = TILESIZE,
        height: int = TILESIZE;

    can postinit;
}

""""
Object class for attacks by the player
"""
obj Attack :pygame.sprite.Sprite: {
    has game: Game,
        x: int,
        y: int;
    has _layer: int = ATTACK_LAYER,
        width: int = TILESIZE,
        height: int = TILESIZE,
        animation_loop: float = 0;

    can postinit;
    can update;
    can collide;
    can animate;
}

"""
Object class for buttons used in the game (Start, Restart)
"""
obj Button {
    has x: int,
        y: int,
        width: int,
        height: int,
        fg: tuple,
        bg: tuple,
        content: str,
        fontsize: int;

    can postinit;
    can is_pressed(pos: tuple, pressed: tuple) -> bool;
}