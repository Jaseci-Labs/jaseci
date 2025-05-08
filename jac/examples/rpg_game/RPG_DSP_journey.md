# Journey of Building a Zelda-style RPG in JacLang

[Demo Video.webm](https://github.com/Jayanaka-98/py-game-RPG/assets/110921856/1ac069eb-7a07-462f-82fe-a8c1e3481935)

This RPG game is developed using a pre-built base game coded in Python which can be found in [here](./python_impl/).

This is a tutorial on how to build the same game in Jaclang. Two different implementations will be discussed, one taking a more conventional programming approach while the other delving into a more interesting method of programming which is [Data-spatial](#data-spatial-implementation) programming.

- [Journey of Building a Zelda-style RPG in JacLang](#journey-of-building-a-zelda-style-rpg-in-jaclang)
  - [Setting Up](#setting-up)
  - [Explanation on the Structure of the Game](#explanation-on-the-structure-of-the-game)
    - [main](#main)
    - [sprites](#sprites)
    - [config](#config)
    - [map](#map)
  - [Imports: _Cross-language imports?_](#imports-cross-language-imports)
  - [Global Variable Definition](#global-variable-definition)
  - [Game Code: main.jac](#game-code-mainjac)
  - [Programming Sprites and Level objects](#programming-sprites-and-level-objects)
  - [Data Spatial Implementation](#data-spatial-implementation)
    - [Data Spatial architecture](#data-spatial-architecture)
  - [Converting RPG into Data-spatial Architecture](#converting-rpg-into-data-spatial-architecture)
    - [game\_obj.jac](#game_objjac)
    - [sprite.jac, config.jac \& map.jac](#spritejac-configjac--mapjac)
    - [Runtime Logic of the program : main\_dsp.jac](#runtime-logic-of-the-program--main_dspjac)
      - [Nodes and Walkers](#nodes-and-walkers)
      - [Start Screen node](#start-screen-node)
      - [Level node](#level-node)
      - [Game Walker](#game-walker)
      - [Initiating the Graph (Begin Runtime)](#initiating-the-graph-begin-runtime)

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

![The architecture](./Diagrams/RPG%20Space%20-%20Game%20Architecture.png)

### main

The main game structures lie within the main.jac file where we can construct intro screens, levels, game over screens, and loading screens. The game runtime logic structure is written in this code section as well as the initiation of the game instance. The sprites.py, config.py, and map.py will be imported in order to function the game.

### sprites

As shown in the above diagram the main.jac file uses the objects defined inside the sprites.jac file. The game has been developed utilizing the pygame library. These objects are known as sprites where there is an assigned character, actions and animations can be called upon.
All in-game sprite models are created within this file.

### config

Configuration parameters such as window size. layer order is stored in this file. By changing these parameters it is able to modify key game configurations without altering the main game structure.

### map

Contains the map of the game which can be changed as required.

- B : Blocks (Walls)
- E : Enemy Spawn Point
- P : Player Spawn Point

The structure of the map is shown in the diagram above. It is possible to maintain a directory of many level maps, but as for the scope of this project, the same map will be used for development.

## Imports: _Cross-language imports?_

When programming with **Python** or any other programming language, modules or libraries have a key importance as they extend the capabilities of the base language using pre-programmed classes and methods.

In **Jaclang** in addition to the libraries written specifically for the language, any python module can also be imported when programming with Jaclang.

```python
# Importing Python modules
import pygame;
import sys;

# Including Jac codebase
import sprites;
import config;
import map;
```

> **Syntax Note:**
>
> - If a specific python module needs to be imported:
>
>    ```import module;```
> - If a specific submodule needs to be imported from a module:
>
>    ```import from module, submodule_1 submodule_2;```

## Global Variable Definition

When defining variables they should be coupled with a prefix that describes the environment the variable resides in. Additionally, the type annotation should be included for well typed code.

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

> **Syntax Note:**
>
> - When comparing with pythonic coding style, the type annotation and line delimiting with ';' can be noted which leads to a more readable code.

## Game Code: main.jac

The main sections of the game are defined in the main.jac file. There are main four sections of the game. To initiate the pygame module various fields must be defined for our game object.

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

> **Syntax Note:**
>
> - Here the fields of this class are defined using ```has``` keyword. This symbolizes that the specified 'obj' 'has' the said variable.

In Jaclang, an ```__init__``` function is not required as the field variables and input parameters(if any) will auto generate and execute an initialization function in the background.

Although an ```__init__``` function is not required by the programmer, there are such cases where some other tasks require to be performed just after ```__init__```. These tasks can be performed in Jaclang with ```postinit``` which will be called after(post) the initialization function.

```python
    ...
    can postinit {
    can postinit {
        pygame.<>init();
        self.font: pygame.font.Font=pygame.font.Font(GENERAL_FONT, 32);
    }
    ...
```

> **Syntax Note:**
>
> - Functions in jaclang are defined such that the ```def``` keyword is substituted with ```can``` keyword which improves the human readability of the code as 'can' depicts an ability of an object.
> - The Jaclang keyword for the python ```__init__``` is just ```ìnit```, which can be confusing for the interpreter if a function is defined as ```ìnit()```. This is the case with pygame module. Here, to avoid triggering an unwanted initialization, keyword escape '<>' is used as shown above. This will ignore the ```__init__``` and run the defined function, ```ìnit()```.

After initializing the object, the functions/methods of the game class can be defined. In the code snippet below, we declare all the required functions without defining the functionality of those abilities.

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

> **Syntax Note:**
>
> - In Jaclang, function names and their passable parameters can be defined without the full implementation of the function, which allows a cleaner body inside the object class. The definitions can be written in any of the imported code files.

In Python, we use the main body of a .py file to code the runtime logic of the operation. In contrast, Jaclang uses ```with entry {}``` syntax to enclose the runtime code within parenthesis.

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

Having the objects & method definitions as well as the runtime logic readable with minimal clutter is beneficial to understanding the functionality of the program without going through tedious code implementations.

The implementation of the above game class can be done as below in any of the imported files.

```python
:obj:Game:can:createTilemap {
    for (i, row) in enumerate(tilemap) {
        for (j, column) in enumerate(row) {
            Ground(self, j, i);
            if column == "B" {
                Block(self, j, i);
            }
            if column == "E" {
                Enemy(self, j, i);
            }
            if column == "P" {
                self.player = Player(self, j, i);
            }
        }
    }
}
```

> **Syntax Note:**
>
> - Here the syntax is such that, for a can(def) function within an obj(class),
>
>      ```:obj:<obj_name>:can:<func_name>(params){body}```
>
> - Therefore, the entire codebase implementation can be written in different files and the program will work as long as the files are imported in the module that will ```jac run```. To include the relevent file to the module, we can
>
>      ```:obj:<obj_name>:can:<func_name>(params){body}```
>
>   before using the imported implementations.

```python
# Start a new game

:obj:Game:can:new {
    self.playing = True;
    self.won = False;
    self.all_sprites = pygame.sprite.LayeredUpdates();
    self.blocks = pygame.sprite.LayeredUpdates();
    self.enemies = pygame.sprite.LayeredUpdates();
    self.attacks = pygame.sprite.LayeredUpdates();
    self.createTilemap();
}
# Update pygame events to check if the game is quitted or attacked.

:obj:Game:can:events {
    for events in pygame.event.get() {
        if events.type == pygame.QUIT {
            self.playing = False;
            self.running = False;
        }
        keys = pygame.key.get_pressed();
        ...
    }
}
# Update all sprites

:obj:Game:can:update {
    ...
# Display the game

:obj:Game:can:draw {
    ...
}
# Game runtime

:obj:Game:can:main {
    ...
}
# Game over screen

:obj:Game:can:game_over() {
    ...
}
# Introduction Screen

:obj:Game:can:intro_screen {
    ...
}
# Game won

:obj:Game:can:game_won {
    ...
}
```

The complete codebase is programmed similarly which is included in [main.jac](.//jac_impl/jac_impl_3/main.jac).

## Programming Sprites and Level objects

The pygame environment is built in a separate [sprites.jac](.//jac_impl/jac_impl_3/sprites.jac) file for better codebase management.

There are mainly five different level object models that need to be programmed. Namely,

- Spritesheet : Extract and manage sprite images
- Player : Player Character
- Enemy : Enemy Characters
- Ground : Ground layer
- Block : Obstacles
- Attack : Sword slashes from the player

```python
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
    ...
}

"""
Object for blocks (Walls) with type pygame.sprite.Sprite
"""
obj Block :pygame.sprite.Sprite: {
    ...
}

"""
Object for ground with type pygame.sprite.Sprite
"""
obj Ground :pygame.sprite.Sprite: {
    ...
}

""""
Object class for attacks by the player
"""
obj Attack :pygame.sprite.Sprite: {
    ...
}

"""
Object class for buttons used in the game (Start, Restart)
"""
obj Button {
    ...
}
```

The implementation of these objects can be found in [sprites.jac](<.//jac_impl/jac_impl_3/sprites.jac>). The implementations are exactly similar to the implementations previously done in the main.jac file.

## Data Spatial Implementation

The previously discussed implementations are how a conventional programmer would use Jaclang to program a relatively complex program using object-oriented programming paradigm.

In this section we will discuss on how to code the above program using a novel inbuilt prgaramming paradigm in jac-lang, which is **Data-spatial Programming**.

### Data Spatial architecture

Graph theory is one of the theories at the forefront of conceptual innovation. Almost all modern constructs such as programs and networks can be represented using graphs with functions acting as graph traversal entities.

There are two main constructs in graphs: **nodes** and **edges**. Taking our RPG into consideration a node can be represented by a single level instance and edges represent the progression of the game. This graph like structure is depicted in the diagram below(Right).

![DSP](./Diagrams/RPG%20Space%20-%20DSP.png)

There is another construct that needs to be discussed which is **walkers**. In the RPG, the player must play through the levels in order to progress. This graph traversal is done by an agent who is the player. This graph traversal agent is known as a "walker". Walkers can walk on the graph in any specified manner and can perform different abilities upon entry or exit from a node.

When programming the RPG using OOP, after a level has been won or lost, the immediately previous game level data will be lost unless saved separately on a global variable.

In a data-spatial implementation of the game architecture, after a level has been won it will create a new level node on the graph and when a game is lost it will go back on the graph and branch off to create a new instance of the game level, leaving all previous level data untouched.

This ability is important when the program is required to fetch pevious playthrough data to procedurally generate maps using the playing patterns on the player.

## Converting RPG into Data-spatial Architecture

The game built in the conventional program can be converted into the data spatial architecture with some additional changes. The advantage in using jac-lang for data-spatial programming is that it is not required to convert the entire program into data-spatial architecture for it to work as a data-spatial program. Conventional OOP code segments can run within nodes or walkers which makes this a hibrid programming model.

The fully implemented Data-spatial version can be found at [jac_impl_4](.//jac_impl/jac_impl_4/) if you want to jump in straight.

### game_obj.jac

This is a direct copy of the main.jac file in previous implementations. The only difference in this file is the runtime logic has been removed from here. This is because the main difference in this data-spatial implementation is that the program runtime runs as a graph. Nothing else needs to happen in this file.

### sprite.jac, config.jac & map.jac

No changes are required on these files as well.

### Runtime Logic of the program : [main.jac](.//jac_impl/jac_impl_4/main.jac)

This new file will include the supporting architecture for the build of the data-spatial implementation and the runtime logic for graph traversal.

```python
import pygame;
import sys;
import random;

import sprites;
import config;
import map;
import game_obj;
```

Now the visualization of the graph is really important in order to build the architecture.

![Game DSP Impl](./Diagrams/RPG%20Space%20-%20DSP%20Architecture%20of%20RPG.png)

#### Nodes and Walkers

When the game starts, it will visualize the intro screen with a button to start a new game. This should trigger a function to create a new level and the game should start on new level. In the case when the player loses the first level he will go back to the start screen, but it will not be visualized as the functionality must be skipped. When losing the level somewhere down the graph, the player will simply come up one level skip the level and continue to a new instance of the lost level.

For this it can be observed we need two nodes and one walker types.

```python
'''Start screen node which operate as the virtual root node'''
node start_screen {
    ...
}

'''Level node which containes the runtime of a level'''
node level {
    ...
}

'''The walker that initiates the game and runs an instance of the game'''
walker game {
    ...
}
```

#### Start Screen node

The start screen node should be able to visualize the start screen when the ```game``` walker enters the ````start_screen``` node, and exit the game if the player has pressed the quit button on the game. Encapsulating these abilities and a variable to check if the game has started, we can declare the node object.

```python
node start_screen {
    has game_started: bool = False;

    can intro_screen with game entry;
    can exit_game with game exit;
}
```

> **Syntax Note:**
>
> - here when declaring when an ability should run (with exit or with entry of a walker), the ```with``` keyword is used following with whether it is ```entry``` or ```exit```.

#### Level node

On the other hand, the level node should have the ability to run the game level on that node, and it also should be able to detect whether the player has pressed the exit button. Additionally, each level should have a unique identifier and a level number along with the information on whether the level instance was previously played, and its level map.

```python
node level {
    has game_level: int = 1,
        level_id: str = '1_1000',
        played: bool = False,
        levelmap: list[str] = Map();

    can run_game with game entry;
    can exit_game with game exit;
}

```

#### Game Walker

The ```game``` walker is the traversal agent that triggers the abilities in nodes. However, the methodology on how this walker should move from node to node can be either defined on the walker itself or on the nodes. In the case of this game, it is defined on the nodes, hence we need it to continue from the ```root``` node after initializing pygame to start the game.

```python
walker game {
    has g: Game = None,
        fwd_dir: bool = True;

    can start_game with `root entry;
}
```

#### Initiating the Graph (Begin Runtime)

In the previous implementation, we used ```with entry {}``` to begin the program. Here also we are doing the same. But, rather than running the game from there, we are just placing the ```game``` walker on the ```root``` node, which starts the game.

```python
with entry {
    root spawn game();
}
```

<!-- TODO: need to add impl 5 and 6 -->
