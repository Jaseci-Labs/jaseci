# Journey of Building a Zelda-style RPG in JacLang

[Demo Video.webm](https://github.com/Jayanaka-98/py-game-RPG/assets/110921856/1ac069eb-7a07-462f-82fe-a8c1e3481935)

This RPG game is developed using a pre-built base game coded in python which can be found in [here](./python_impl/).

This is a tutorial on how to build the same game in Jaclang. Two different implementations will be discussed, one taking a more conventional programming approach while the other delving into a more interesting method of programming which is [Data-spatial](#data-spatial-implementation) programming

- [Journey of Building a Zelda-style RPG in JacLang](#journey-of-building-a-zelda-style-rpg-in-jaclang)
  - [Setting Up](#setting-up)
  - [Explanation on the Structure of the Game](#explanation-on-the-structure-of-the-game)
    - [main](#main)
    - [sprites](#sprites)
    - [config](#config)
    - [map](#map)
  - [Imports: _Cross-language modules?_](#imports-cross-language-modules)
  - [Global Variable Definition](#global-variable-definition)
  - [Game Code: main.jac](#game-code-mainjac)
  - [Programming Sprites and Level objects](#programming-sprites-and-level-objects)
  - [Data Spatial Implementation](#data-spatial-implementation)

## Setting Up

In order for the following requirements should be met.

- Python 3.11 or newer
- Jaclang newest available version
```
$ pip install jaclang
```
- pygame newest available version
```
$ pip install pygame
```

## Explanation on the Structure of the Game

The game is essentially a playable character on a map having the ability of attacking any enemy who are nearby. Enemies are placed according to the map configuration and the game is won when all the enemies are killed. The game uses the pygame library to create animation and enable gameplay. The game is written under four files to improve readability and codebase management.

![The architecture](.//jac_impl/RPG%20Space%20-%20Game%20Architecture.png)

### main

The main game structures lie within the main.jac file where we can construct intro screens, levels, game over screens and loading screens. The game runtime logic structure is written in this code section as well as the initiation of the game instance. The sprites.py, config.py and map.py will be imported in order to function the game.

### sprites

As shown in the above diagram the main.jac file uses the objects defined inside the sprites.jac file. The game has been developed utilizing the pygame library. These objects are known as sprites where there is an assigned character, actions and animations can be called upon.
All in game sprite models are created within this file.

### config

Configuration parameters such as window size. layer order is stored in this file. By changing these parameters it is able to modify key game configurations without altering the main game structure.

### map

Contains the map of the game which can be changed as required.

- B : Blocks (Walls)
- E : Enemy Spawn Point
- P : Player Spawn Point

The structure of the map is shown on the above diagram. It is possible to maintain a directory of many level maps, but as for the scope of this project the same map will be used for development.

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
...
glob BLUE:tuple = (0, 0, 255);
glob WHITE:tuple = (255, 255, 255);
...
glob GENERAL_FONT:str = '../<.tf font file location>';
```
The full global variable definition can be found in [config.jac](..//rpg_game/jac_impl/jac_impl_3/config.jac) and [map.jac](../rpg_game/jac_impl/jac_impl_3/map.jac)

> **Syntax Note:** When comparing with pythonic coding style, the type annotation and line delimiting with ';' can be noted which leads to a more readable code.

## Game Code: main.jac

The main sections of the game is defined in the main.jac file. There are main four sections of the game. To initiate the pygame module various fields must be defined for our game object.

```python
obj Game {
    has screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)),
        clock: pygame.time.Clock = pygame.time.Clock(),
        running: bool = True,
        ...
        attack_spritesheet: Spritesheet = Spritesheet('../img/attack.png'),
        intro_background: pygame.surface.Surface = pygame.image.load('../img/introbackground.png'),
        go_background: pygame.surface.Surface = pygame.image.load('../img/gameover.png');

    ...
```

> **Syntax Note:** Here the fields of this class is defined using has keyword. This symbolizes that the specified 'obj' 'has' the said variable.

In Jaclang, an ```__init__``` function is not required as the field variables and input parameters(if any) will auto generate and execute an initialization function in the background.

Although an ```__init__``` function is not required by the programmer, there are such cases where some other tasks requires to be performed just after ```__init__```. These tasks can be performed in Jaclang with ```postinit``` which will be called after(post) the init function.

```python
    ...
    can postinit {
        pygame.init();
        <self>.font: pygame.font.Font=pygame.font.Font(GENERAL_FONT, 32);
    }
    ...
```

> **Syntax Note:** functions in jaclang is defined such that the ```def``` keyword is substituted with ```can``` keyword which improves the human readability of the code as 'can' depicts an ability of an object.

After initializing the object, the functions/methods of the game class can be defined. In the below code snippet we declare all the required functions without defining the functionality of those abilities.

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

> **Syntax Note:** in Jaclang, function names and their passable parameters can be defined without the full implementation of the function, which allows a cleaner body inside the object class. The definitions can be written any of the included code base locations.

In Python we use the main body of a .py file to code the runtime logic of the operation. In contrast, Jaclang uses ```with entry {}``` syntax to enclose the runtime code within parenthesis.

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

The implementation of the above game class can be done as below on any of the included codebase locations.

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
> **Syntax Note:** Here the syntax is such that, for a can(def) function within an obj(class), ```:obj:<obj_name>:can:<func_name>(params){body}```

The rest of the codebase is programmed in a similar manner which is included in [main.jac](.//jac_impl/jac_impl_3/main.jac).

## Programming Sprites and Level objects

The pygame environment is built in a separate sprites.jac file for better codebase management.

There are mainly five different level object models that needs to be programmed. Namely,

- Spritesheet : Extract and manage sprite images
- Player : Player Character
- Enemy : Enemy Characters
- Ground : Ground layer
- Block : Obstacles
- Attack : Sword slashes from the player

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

![DSP](.//jac_impl/RPG%20Space%20-%20DSP.png)
