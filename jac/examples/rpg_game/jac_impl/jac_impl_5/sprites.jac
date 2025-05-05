"""This file containes all definitions of sprites that apear in the game"""


# Importing python libraries
import pygame;
import from pygame.sprite { AbstractGroup }
import random;
import math;
# Importing configuration and map data
import config;
import map;
import from typing { Tuple }

"""
Object for impoting sprite character images.
"""
obj Spritesheet {
    can init(file: str);
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

:obj:Spritesheet:can:init
(file: str) {
    self.sheet = pygame.image.load(file).convert();
}

:obj:Spritesheet:can:get_sprite
(x: int, y: int, width: int, height: int) {
    sprite = pygame.Surface([width, height]);
    sprite.blit(self.sheet, (0, 0), (x, y, width, height));
    sprite.set_colorkey(BLACK);
    return sprite;
}

:obj:Player:can:postinit {
    self._layer = PLAYER_LAYER;
    self._groups = self.game.all_sprites;
    pygame.sprite.Sprite.init(self, self._groups);
    self.x*=TILESIZE;
    self.y*=TILESIZE;
    self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width-5, self.height-5);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
}
# Update the player actions

:obj:Player:can:update {
    self.movement();
    self.animate();
    self.collide_enemy();
    self.rect.x+=self.x_change;
    self.collide_blocks('x');
    self.rect.y+=self.y_change;
    self.collide_blocks('y');
    self.x_change = 0;
    self.y_change = 0;
}
# Movement controls based on arrow key pushes.

:obj:Player:can:movement {
    keys = pygame.key.get_pressed();
    if keys[pygame.K_LEFT] {
        for sprite in self.game.all_sprites {
            sprite.rect.x+=PLAYER_SPEED;
        }
        self.x_change-=PLAYER_SPEED;
        self.facing = 'left';
    }
    if keys[pygame.K_RIGHT] {
        for sprite in self.game.all_sprites {
            sprite.rect.x-=PLAYER_SPEED;
        }
        self.x_change+=PLAYER_SPEED;
        self.facing = 'right';
    }
    if keys[pygame.K_UP] {
        for sprite in self.game.all_sprites {
            sprite.rect.y+=PLAYER_SPEED;
        }
        self.y_change-=PLAYER_SPEED;
        self.facing = 'up';
    }
    if keys[pygame.K_DOWN] {
        for sprite in self.game.all_sprites {
            sprite.rect.y-=PLAYER_SPEED;
        }
        self.y_change+=PLAYER_SPEED;
        self.facing = 'down';
    }
}
# Player death when collidong with an enemy.

:obj:Player:can:collide_enemy {
    hits = pygame.sprite.spritecollide(self, self.game.enemies, False);
    if hits {
        self.kill();
        self.game.playing = False;
    }
}
# Anminate the player character.

:obj:Player:can:animate {
    down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height), self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height), self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)];
    up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height), self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height), self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)];
    left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height), self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height), self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)];
    right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height), self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height), self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)];
    if self.facing == "down" {
        if self.y_change == 0 {
            self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height);
        } else {
            self.image = down_animations[math.floor(self.animation_loop)];
            self.animation_loop+=0.1;
            if self.animation_loop >= 3 {
                self.animation_loop = 1;
            }
        }
    }
    if self.facing == "up" {
        if self.y_change == 0 {
            self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height);
        } else {
            self.image = up_animations[math.floor(self.animation_loop)];
            self.animation_loop+=0.1;
            if self.animation_loop >= 3 {
                self.animation_loop = 1;
            }
        }
    }
    if self.facing == "right" {
        if self.x_change == 0 {
            self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height);
        } else {
            self.image = right_animations[math.floor(self.animation_loop)];
            self.animation_loop+=0.1;
            if self.animation_loop >= 3 {
                self.animation_loop = 1;
            }
        }
    }
    if self.facing == "left" {
        if self.x_change == 0 {
            self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height);
        } else {
            self.image = left_animations[math.floor(self.animation_loop)];
            self.animation_loop+=0.1;
            if self.animation_loop >= 3 {
                self.animation_loop = 1;
            }
        }
    }
}
# Ability to collide with blocks without passing through.

:obj:Player:can:collide_blocks
(direction: str) {
    if direction == "x" {
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False);
        if hits {
            if self.x_change > 0 {
                self.rect.x = hits[0].rect.left - self.rect.width;
                for sprite in self.game.all_sprites {
                    sprite.rect.x+=PLAYER_SPEED;
                }
            }
            if self.x_change < 0 {
                self.rect.x = hits[0].rect.right;
                for sprite in self.game.all_sprites {
                    sprite.rect.x-=PLAYER_SPEED;
                }
            }
        }
    }
    if direction == "y" {
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False);
        if hits {
            if self.y_change > 0 {
                self.rect.y = hits[0].rect.top - self.rect.height;
                for sprite in self.game.all_sprites {
                    sprite.rect.y+=PLAYER_SPEED;
                }
            }
            if self.y_change < 0 {
                self.rect.y = hits[0].rect.bottom;
                for sprite in self.game.all_sprites {
                    sprite.rect.y-=PLAYER_SPEED;
                }
            }
        }
    }
}

:obj:Enemy:can:postinit {
    self._groups = (self.game.all_sprites, self.game.enemies);
    pygame.sprite.Sprite.__init__(self, self._groups);
    self.x*=TILESIZE;
    self.y*=TILESIZE;
    self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height);
    self.facing = random.choice(['up', 'down', 'left', 'right']);
    self.max_travel = random.randint(7, 30);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
}
# Update the enemy actions

:obj:Enemy:can:update {
    self.movement();
    self.animate();
    self.rect.x+=self.x_change;
    self.collide_blocks('x');
    self.rect.y+=self.y_change;
    self.collide_blocks('y');
    self.x_change = 0;
    self.y_change = 0;
}
# Movement controls.

:obj:Enemy:can:movement {
    if self.facing == 'left' {
        self.x_change-=ENEMY_SPEED;
        self.movement_loop-=1;
        if self.movement_loop <= -self.max_travel {
            self.facing = 'right';
        }
    }
    if self.facing == 'right' {
        self.x_change+=ENEMY_SPEED;
        self.movement_loop+=1;
        if self.movement_loop >= self.max_travel {
            self.facing = 'left';
        }
    }
    if self.facing == 'up' {
        self.y_change+=ENEMY_SPEED;
        self.movement_loop+=1;
        if self.movement_loop >= self.max_travel {
            self.facing = 'down';
        }
    }
    if self.facing == 'down' {
        self.y_change-=ENEMY_SPEED;
        self.movement_loop-=1;
        if self.movement_loop <= -self.max_travel {
            self.facing = 'up';
        }
    }
}
# Anminate the enemy character.

:obj:Enemy:can:animate {
    down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height), self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height), self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)];
    up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height), self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height), self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)];
    left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height), self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height), self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)];
    right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height), self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height), self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)];
    if self.facing == "down" {
        self.image = down_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.1;
        if self.animation_loop >= 3 {
            self.animation_loop = 1;
        }
    }
    if self.facing == "up" {
        self.image = up_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.1;
        if self.animation_loop >= 3 {
            self.animation_loop = 1;
        }
    }
    if self.facing == "right" {
        self.image = right_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.1;
        if self.animation_loop >= 3 {
            self.animation_loop = 1;
        }
    }
    if self.facing == "left" {
        self.image = left_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.1;
        if self.animation_loop >= 3 {
            self.animation_loop = 1;
        }
    }
}
# Ability to collide with blocks without passing through.

:obj:Enemy:can:collide_blocks
(direction: str) {
    if direction == "x" {
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False);
        if hits {
            if self.x_change > 0 {
                self.rect.x = hits[0].rect.left - self.rect.width;
            }
            if self.x_change < 0 {
                self.rect.x = hits[0].rect.right;
            }
        }
    }
    if direction == "y" {
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False);
        if hits {
            if self.y_change > 0 {
                self.rect.y = hits[0].rect.top - self.rect.height;
            }
            if self.y_change < 0 {
                self.rect.y = hits[0].rect.bottom;
            }
        }
    }
}

:obj:Block:can:postinit {
    self._groups = (self.game.all_sprites, self.game.blocks);
    pygame.sprite.Sprite.init(self, self._groups);
    self.x*=TILESIZE;
    self.y*=TILESIZE;
    self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
}

:obj:Ground:can:postinit
(game: None, x: int, y: int) {
    self._groups = self.game.all_sprites;
    pygame.sprite.Sprite.init(self, self._groups);
    self.x*=TILESIZE;
    self.y*=TILESIZE;
    self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
}

:obj:Attack:can:postinit {
    self._groups = (self.game.all_sprites, self.game.attacks);
    pygame.sprite.Sprite.init(self, self._groups);
    self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
}
# Update the attack interations

:obj:Attack:can:update {
    self.animate();
    self.collide();
}
# Ability to collide with enemies without passing through.

:obj:Attack:can:collide {
    hits = pygame.sprite.spritecollide(self, self.game.enemies, True);
}
# Anminate the attacks.

:obj:Attack:can:animate() {
    direction = self.game.player.facing;
    right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height), self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height), self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height), self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height), self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)];
    down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height), self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height), self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height), self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height), self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)];
    left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height), self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height), self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height), self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height), self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)];
    up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height), self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height), self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height), self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height), self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)];
    if direction == 'up' {
        self.image = up_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.5;
        if self.animation_loop >= 5 {
            self.kill();
        }
    }
    if direction == 'down' {
        self.image = down_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.5;
        if self.animation_loop >= 5 {
            self.kill();
        }
    }
    if direction == 'left' {
        self.image = left_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.5;
        if self.animation_loop >= 5 {
            self.kill();
        }
    }
    if direction == 'right' {
        self.image = right_animations[math.floor(self.animation_loop)];
        self.animation_loop+=0.5;
        if self.animation_loop >= 5 {
            self.kill();
        }
    }
}

:obj:Button:can:postinit {
    self.font = pygame.font.Font(GENERAL_FONT, self.fontsize);
    self.image = pygame.Surface((self.width, self.height));
    self.image.fill(self.bg);
    self.rect = self.image.get_rect();
    self.rect.x = self.x;
    self.rect.y = self.y;
    self.text = self.font.render(self.content, True, self.fg);
    self.text_rect = self.text.get_rect(center=(self.width / 2, self.width / 2));
    self.image.blit(self.text, self.text_rect);
}
# Determine if thebutton is pressed.

:obj:Button:can:is_pressed
(pos: tuple, pressed: tuple) {
    if self.rect.collidepoint(pos) {
        if pressed[0] {
            return True;
        }
        return False;
    }
    return False;
}
