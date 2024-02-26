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

The game is esentially a playable character on a map which the ability of attacking any anemy who are nearby. Enemies are placed accoding to the map configuration and when all the enemies are killed the game is won.

### main.py

This file contains the main game code which describes the functionality of the game. The game runtime logic structure is written in this code section as well as the intiation of the game instance. The sprites.py, config.py and map.py will be imported in order to propoerly function the game.

### sprites.py

The game has been developed utilizing the pygame library. Each and every game object is of custom class 'sprite' included within the pygame library.
All in game sprite models are created within this code.

### config.py

Configuration parameters such as windowsize. layer order is stored inthis file.

### map.py

Contains the map of the game which can be changed as required.

- B : Blocks (Walls)
- E : Enemy Spawn Point
- P : Player Spawn Point

## Imports: _Cross-language modules?_

When programming with **Python** or any other programming language, modules or libraries have a key importace as they extend the capabilities of the base language using pre programmed classes and methods.

In **Jaclang** additionally to the libraries written specifically for the language, any python module can also be imported when programming with Jaclang.

```python
# Importing Python modules
import:py pygame;
import:py sys;
import:py from math, sqrt;

# Including Jac codebase
include:jac sprites;
include:jac config;
include:jac map;
```

## Variable Definition

When defining variables they should be coupled with a prefix which describes the environment the variable resides in. Additionally the type annotation.

In the below code snippet global variables are defined using the _glob_ prefix  and their type annotations.

```python
glob WIN_WIDTH:int = 640;
glob WIN_HEIGHT:int = 480;
glob TILESIZE:int = 32;
glob FPS:int = 60;
...
glob RED:tuple = (255, 0, 0);
glob BLACK:tuple = (0, 0, 0);
glob BLUE:tuple = (0, 0, 255);
```

## Classes and Objects

