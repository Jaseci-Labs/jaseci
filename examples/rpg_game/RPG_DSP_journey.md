# Journey of Building an Zelda-style RPG in JacLang

[Demo Video.webm](https://github.com/Jayanaka-98/py-game-RPG/assets/110921856/1ac069eb-7a07-462f-82fe-a8c1e3481935)

This RPG game is developed using a pre-built base game coded in python which can be found in [here](/home/jayanaka-98/jaclang/examples/rpg_game/python_impl).

The RPG game was then implemented in jaclang in several iterations.

## Setting Up

In order for these implementations to work, the following requirements should be met.

- Python 3.11 or newer
- Jaclang newest available version
```
$ pip install jaclang
```
- pygame newest available version
```
$ pip install pygame
```

## Explantion on the Structure of the Game

The game is essentially a playable character on a map which the ability of attacking any enemy who are nearby. Enemies are placed according to the map configuration and when all the enemies are killed the game is won.

### main.py

This file contains the main game code which describes the functionality of the game. The game runtime logic structure is written in this code section as well as the initiation of the game instance. The sprites.py, config.py and map.py will be imported in order to properly function the game.

### sprites.py

The game has been developed utilizing the pygame library. Each and every game object is of custom class 'sprite' included within the pygame library.
All in game sprite models are created within this code.

### config.py

Configuration parameters such as windowsize. layer order is stored in this file.

### map.py

Contains the map of the game which can be changed as required.

- B : Blocks (Walls)
- E : Enemy Spawn Point
- P : Player Spawn Point

## Imports: _Cross-language modules?_

When programming with **Python** or any other programming language, modules or libraries have a key importance as they extend the capabilities of the base language using pre-programmed classes and methods.

In **Jaclang** additionally to the libraries written specifically for the language, any python module can also be imported when programming with Jaclang.

```python
# Importing Python modules
import:py pygame;
import:py sys;

# Including Jac codebase
include:jac sprites;
include:jac config;
include:jac map;
```

## Global Variable Definition

When defining variables they should be coupled with a prefix which describes the environment the variable resides in. Additionally, the type annotation should be included for a well typed code.

In the below code snippet global variables are defined using the _glob_ prefix and their type annotations.

```python
glob WIN_WIDTH:int = 640;
glob WIN_HEIGHT:int = 480;
glob TILESIZE:int = 32;
glob FPS:int = 60;

glob ATTACK_LAYER:int = 5;
glob ENEMY_LAYER:int = 4;
glob PLAYER_LAYER:int = 3;
glob BLOCK_LAYER:int = 2;
glob GROUND_LAYER:int = 1;

glob PLAYER_SPEED:int = 3;
glob ENEMY_SPEED:int = 2;

glob RED:tuple = (255, 0, 0);
glob BLACK:tuple = (0, 0, 0);
glob BLUE:tuple = (0, 0, 255);
glob WHITE:tuple = (255, 255, 255);

glob GENERAL_FONT:str = '../<.tf font file location>';

glob tilemap:List[str] = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..E...............B',
    'B..................B',
    'B....BBBB......E...B',
    'B..................B',
    'B..................B',
    'B.........P........B',
    'B..................B',
    'B....E.............B',
    'B..................B',
    'B.......BBB........B',
    'B.........B........B',
    'B.........B....E...B',
    'B.........B........B',
    'BBBBBBBBBBBBBBBBBBBB'

];
```

## Game Code: main.jac

Here we are defining the game class which is the main body of the game.

```python
obj Game {
    has screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)),
        clock: pygame.time.Clock = pygame.time.Clock(),
        running: bool = True,
        won: bool = False,
        score: int = 0,
        deaths: int = 0,
        character_spritesheet: Spritesheet = Spritesheet('../img/character.png'),
        terrain_spritesheet: Spritesheet = Spritesheet('../img/terrain.png'),
        enemy_spritesheet: Spritesheet = Spritesheet('../img/enemy.png'),
        attack_spritesheet: Spritesheet = Spritesheet('../img/attack.png'),
        intro_background: pygame.surface.Surface = pygame.image.load('../img/introbackground.png'),
        go_background: pygame.surface.Surface = pygame.image.load('../img/gameover.png');

    ...
```

Here the fields of this class is defined using has keyword. This symbolyses that the specified 'obj' 'has' the said variable.

In Jaclang, an **init** function is not required as the field variables and input parameters(if any) will auto generate and execute an initialization function in the background. Object parameters are defined variables under 'has' prefix. But in order to initialize the pygame.init() we need a function that runs just after running init which is <post_init>.

```python
    ...
    can <post_init> {
        pygame.init();
        <self>.font: pygame.font.Font=pygame.font.Font(GENERAL_FONT, 32);
    }
    ...
```

After initializing the functions/methods of the game class can be defined. Another cutting edge feature of Jaclang is that it is possible to separate the location of an ability(method) definition and its' implementation which will become useful to improve the readability of programs.

```python
    ...
    can createTilemap; # Generate the map according to the tilemap variable in map.jac
    can new; # Start a new game level
    can events;
    can update;
    can draw;
    can main; # Main runtime of the game level
    can intro_screen; # Intro Screen
    can game_won; # Screen after level has been won
    can game_over; # Screen after level has been lost
}
```

Here, only the function names are defined which allows a cleaner body inside the object class.

In python we use the main body of a .py file to code the runtime logic of the operation. In contrast, Jaclang uses **with** _entry_ {} syntax to enclose the runtime code within parenthesis.

```python
with entry {
    g = Game();
    g.intro_screen();
    g.new();
    while g.running {
        g.main();
        if g.won == True {
            g.game_won();
        } else {
            g.game_over();
        }
    }
    pygame.quit();
    sys.exit();
}
```

Having the objects & method definitions as well as the runtime logic readable with minimal clutter is beneficial to understand the functionality of the program without going through tedious code implementations.

However, the implementation needs to be done somewhere. In Jaclang, this can be any of the included files which is a feature that is highly valuable to maintain a highly readable and developer friendly codebase.

The implementation of the above game class can be shown below.

```python
:obj:Game:can:createTilemap {
    for (i, row) in enumerate(tilemap) {
        for (j, column) in enumerate(row) {
            Ground(<self>, j, i);
            if column == "B" {
                Block(<self>, j, i);
            }
            if column == "E" {
                Enemy(<self>, j, i);
            }
            if column == "P" {
                <self>.player = Player(<self>, j, i);
            }
        }
    }
}
```

Here the syntax is such that, for a can(def) function within an obj(class),

- :**obj**:<*obj_name*>:**can**:<*func_name*>(params){body}

Therefore, the entire codebase implementations can be written in different files and the program will work as long as the files are included in the file that will run.

The rest of the codebase is programmed in a similar manner.

```python
# Start a new game

:obj:Game:can:new {
    <self>.playing = True;
    <self>.won = False;
    <self>.all_sprites = pygame.sprite.LayeredUpdates();
    <self>.blocks = pygame.sprite.LayeredUpdates();
    <self>.enemies = pygame.sprite.LayeredUpdates();
    <self>.attacks = pygame.sprite.LayeredUpdates();
    <self>.createTilemap();
}
# Update pygame events to check if the game is quitted or attacked.

:obj:Game:can:events {
    for events in pygame.event.get() {
        if events.type == pygame.QUIT {
            <self>.playing = False;
            <self>.running = False;
        }
        keys = pygame.key.get_pressed();
        if keys[pygame.K_SPACE] {
            if <self>.player.facing == 'up' {
                Attack(<self>, <self>.player.rect.x, <self>.player.rect.y - TILESIZE);
            }
            if <self>.player.facing == 'down' {
                Attack(<self>, <self>.player.rect.x, <self>.player.rect.y + TILESIZE);
            }
            if <self>.player.facing == 'right' {
                Attack(<self>, <self>.player.rect.x + TILESIZE, <self>.player.rect.y);
            }
            if <self>.player.facing == 'left' {
                Attack(<self>, <self>.player.rect.x - TILESIZE, <self>.player.rect.y);
            }
        }
    }
}
# Update all sprites

:obj:Game:can:update {
    <self>.all_sprites.update();
}
# Display the game

:obj:Game:can:draw {
    <self>.screen.fill(BLACK);
    <self>.all_sprites.draw(<self>.screen);
    <self>.clock.tick(FPS);
    pygame.display.update();
}
# Game runtime

:obj:Game:can:main {
    while <self>.playing {
        <self>.events();
        <self>.update();
        <self>.draw();
        if len(<self>.enemies.sprites()) == 0 {
            <self>.won = True;
            <self>.playing = False;
        }
    }
    if <self>.won == False {
        <self>.playing = False;
    }
}
# Game over screen

:obj:Game:can:game_over() {
    <self>.score-=2;
    text = <self>.font.render('GaMe OvEr', True, RED);
    text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2));
    restart_button = Button(10, WIN_HEIGHT - 135, 120, 125, WHITE, BLACK, 'Restart', 32);
    for sprite in <self>.all_sprites {
        sprite.kill();
    }
    while <self>.running {
        for event in pygame.event.get() {
            if event.type == pygame.QUIT {
                <self>.running = False;
            }
        }
        mouse_pos = pygame.mouse.get_pos();
        mouse_pressed = pygame.mouse.get_pressed();
        if restart_button.is_pressed(mouse_pos, mouse_pressed) {
            <self>.won = False;
            <self>.new();
            break;
        }
        <self>.screen.blit(<self>.go_background, (0, 0));
        <self>.screen.blit(text, text_rect);
        <self>.screen.blit(restart_button.image, restart_button.rect);
        <self>.clock.tick(FPS);
        pygame.display.update();
    }
}
# Introduction Screen

:obj:Game:can:intro_screen {
    intro = True;
    title = <self>.font.render('Spud-nik : SOLO', True, BLUE);
    title_rect = title.get_rect(x=WIN_WIDTH / 2 - 100, y=100);
    play_button = Button(int(WIN_WIDTH / 2 - 50), 200, 100, 100, WHITE, BLACK, 'Play', 32);
    while intro {
        for event in pygame.event.get() {
            if event.type == pygame.QUIT {
                intro = False;
                <self>.running = False;
            }
        }
        mouse_pos = pygame.mouse.get_pos();
        mouse_pressed = pygame.mouse.get_pressed();
        if play_button.is_pressed(mouse_pos, mouse_pressed) {
            intro = False;
        }
        <self>.screen.blit(<self>.intro_background, (0, 0));
        <self>.screen.blit(title, title_rect);
        <self>.screen.blit(play_button.image, play_button.rect);
        <self>.clock.tick(FPS);
        pygame.display.update();
    }
}
# Game won

:obj:Game:can:game_won {
    <self>.score+=5;
    text = <self>.font.render('YOU WON!', True, BLUE);
    text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2));
    restart_button = Button(10, WIN_HEIGHT - 135, 120, 125, WHITE, BLACK, 'Restart', 32);
    for sprite in <self>.all_sprites {
        sprite.kill();
    }
    while <self>.running {
        for event in pygame.event.get() {
            if event.type == pygame.QUIT {
                <self>.running = False;
            }
        }
        mouse_pos = pygame.mouse.get_pos();
        mouse_pressed = pygame.mouse.get_pressed();
        if restart_button.is_pressed(mouse_pos, mouse_pressed) {
            <self>.new();
            break;
        }
        <self>.screen.blit(<self>.intro_background, (0, 0));
        <self>.screen.blit(text, text_rect);
        <self>.screen.blit(restart_button.image, restart_button.rect);
        <self>.clock.tick(FPS);
        pygame.display.update();
    }
}

```


## Programming Sprites and Level objects

The pygame environment is built in a separate sprites.jac file for better codebase management.

There are mainly five different level object models that needs to be programmed. Namely,
- Spritesheet
- Player : Player Character
- Enemy : Enemy Characters
- Ground : Ground layer
- Block : Obstacles
- Attack : Sward slashes from the player

```python
obj Spritesheet {
    can <init>(file: str);
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

    can <post_init>;
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

    can <post_init>;
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

    can <post_init>;
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

    can <post_init>;
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

    can <post_init>;
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
    can <post_init>;
    can is_pressed(pos: tuple, pressed: tuple) -> bool;
}
```

The implementation of these objects can be found [here](<.//jac_impl/jac_impl_3/sprites.jac>).

## Data Spatial Implementation

Another game changing feature of Jaclang is that it can be programmed in a ''Data-spatial' architecture. This interesting programming paradigm is simply put, graph traversal based programming which has nodes that can have certain attributes and abilities that can be triggered by a walker that traverse the graph on edges.

The point of programming in a data-spatial architecture can be explained using the RPG game itself. After a level has been won or lost the immediately previous game level data will be lost unless saved separately on a global variable.

In a data-spatial implementation of the game architecture, after a level has been won it will create a new level node on the graph and when a game is lost it will go back on the graph and branch off to create a new instance of the game level, leaving all previous level data untouched.

This ability is important when programming in the AI based new era. When integrating large language models into programming it may require previous data to generate something new or do a task. Having a graph based programming loop will enable the program to retrieve necessary information when needed. This is clearly depicted in the following graph.

![DSP](https://drive.google.com/uc?id=15LW7dqCsVY9xmnLg0y-lNTvnCFwtKH6G)
