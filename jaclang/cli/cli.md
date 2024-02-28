# **Jac Language Command Line Interface (CLI)**

Jac Language CLI is with a variety of commands to facilitate users. Additionally, Jac language offers users the ability to define custom CLI commands through plugins. This document aims to provide an overview of each command along with clear usage instructions.

> [!TIP]
> Type "help" on Jac CLI and see!

### Click one of the default commands below and see.
- [tool](#tool) , [format](#format) , [run](#run) , [build](#build) , [check](#check) , [enter](#enter) , [test](#test) , [clean](#clean)

# 1. Command `tool`:
### tool
The `tool` command is utilized to execute specific AST tools along with any optional arguments as needed. This command enables users to interact with language-specific command line tools designed to manage the language effectively.
### Usage:
```bash
$ jac tool <jac_tool> <args>
```
  Parameters to execute the tool command:
  - `jac_tool`: The name of the AST tool to execute.
  - `args`: Optional arguments for the specific AST tool.

  ## 1. tool `ir`:
   `ir` tool generates an Abstract Syntax Tree (AST) and SymbolTable tree for a .jac file, or a Python AST for a .py file. `ir` tool is used with `tool` cli command.
  ### Usage
  ```bash
  $ jac tool ir <output> <file_path>
  ```

  ### Parameters to use the ir tool:
- `output_type`: Choose one of the following options:
  - `sym`: Provides the symbol table of the specified .jac file.
  - `sym.`: Generates a dot graph representation of the symbol table for the specified .jac file.
  - `ast`: Displays the Abstract Syntax Tree (AST) of the specified .jac file.
  - `ast.`: Generates a dot graph representation of the AST for the specified .jac file.
  - `pyast`: Generates the Python AST for a .py file or the relevant Python AST for the generated Python code from a .jac file.
  - `py`: Displays the relevant generated Python code for the respective Jac code in a .jac file.
- `file_path`: Path to the .jac or .py file.

  ### Examples
  >To get the symbol table tree of a Jac file:
  >```bash
  >$ jac tool ir sym <file_path>
  >```
  >To generate a dot graph of the symbol table tree for a Jac file:
  >```bash
  >$ jac tool ir sym. <file_path>
  >```
  >To view the AST tree of a Jac file:
  >```bash
  >$ jac tool ir ast <file_path>
  >```

# 2. Command `run`:
### run
The `run` command is utilized to run the specified .jac or .jir file.
### Usage:
```bash
$ jac run <file_path> [main] [cache]
```
  Parameters to execute the tool command:
  - `file_path`: Path of .jac or .jir file to run.
  - `main`: (bool, optional) A flag indicating whether the module being executed is the main module. Defaults to True
  - `cache` :The cache flag to cache
  ### Examples
  >To run file_path Jac file:
  >```bash
  >$ jac run <file_path>
  >```
