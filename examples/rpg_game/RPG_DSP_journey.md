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

In Jaclang, an **init** function is not required as the field variables and input parameters(if any) will auto generate and execute an initialization function in the background. But in order to initialize the pygame.init() we need a function that runs just after running init which is <post_init>.

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
