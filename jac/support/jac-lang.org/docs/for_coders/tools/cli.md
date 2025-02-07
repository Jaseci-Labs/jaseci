# **Jac Language Command Line Interface (CLI)**

Jac Language CLI is with a variety of commands to facilitate users. Additionally, Jac language offers users the ability to define custom CLI commands through plugins. This document aims to provide an overview of each command along with clear usage instructions. Jac CLI can ba accessed using bash commands as well as by bashing ```jac``` which will start the Jac CLI.


## `jac tool`
Jac Language offers language tools to perform various tasks efficiently. The `tool` command is utilized to execute specific language tools along with any optional arguments as needed. This command enables users to interact with language-specific command line tools designed to manage the language effectively.
```bash
$ jac tool <jac_tool> <args>
```
Parameters to execute the tool command:
- `jac_tool`: The name of the language tool to execute.
    - `ir`, `pass_template`, `py_ast_nodes`,  `md_doc`, `automate_ref` are the jac_tools used to handle (Usage instruction is below)
- `args`: Optional arguments for the specific language tool.


> 1.1. jac_tool `ir`:
  `ir` tool generates an Abstract Syntax Tree (AST) and SymbolTable tree for a .jac file, or a Python AST for a .py file. `ir` tool is used with `tool` cli command.
```bash
jac tool ir <output_type> <file_path>
```

*Parameters for `jac tool ir`*

- `output_type`: Choose one of the following options:
- `sym`: Provides the symbol table of the specified .jac file.
- `sym.`: Generates a dot graph representation of the symbol table for the specified .jac file.
- `ast`: Displays the Abstract Syntax Tree (AST) of the specified .jac file.
- `ast.`: Generates a dot graph representation of the AST for the specified .jac file.
- `pyast`: Generates the Python AST for a .py file or the relevant Python AST for the generated Python code from a .jac file.
- `py`: Displays the relevant generated Python code for the respective Jac code in a .jac file.
- `file_path`: Path to the .jac or .py file.



- To get the symbol table tree of a Jac file:
```bash
jac tool ir sym <file_path>
```
- To generate a dot graph of the symbol table tree for a Jac file:
```bash
jac tool ir sym. <file_path>
```
- To view the AST tree of a Jac file:
```bash
jac tool ir ast <file_path>
```


> jac_tool `pass_template`:
  `pass_template` tool generates pass template for jac.
```bash
jac tool pass_template
```


> jac_tool `py_ast_nodes`:
  `py_ast_nodes` tool lists python ast nodes.
```bash
jac tool py_ast_nodes
```


> jac_tool `md_doc`:
  `md_doc` tool generate mermaid markdown doc.
```bash
jac tool md_doc
```


> jac_tool `automate_ref`:
  `automate_ref` tool automates the reference guide generation.
```bash
jac tool automate_ref
```



## `jac run`

The `run` command is utilized to run the specified .jac or .jir file.
```bash
jac run <file_path> [main] [cache]
```
Parameters to execute the run command:
- `file_path`: Path of .jac or .jir file to run.
- `main`: (Optional, bool) A flag indicating whether the module being executed is the main module. Defaults to True
- `cache` :The cache flag to cache
- To run file_path Jac file:
```bash
jac run <file_path>
```



## `jac clean`
The `clean` command is utilized to remove the __jac_gen__ , __pycache__ folders from the current directory recursively.
```bash
jac clean
```
No Parameters needed to execute the clean command



## `jac format`
The `format` command is utilized to run the specified .jac file or format all .jac files in a given directory.
```bash
jac format <file_path/directory_path> [outfile] [debug]
```
  Parameters to execute the format command:
  - `file_path/directory_path`: The path to the .jac file or directory containing .jac files.
  - `outfile`: (Optional) The output file path (only applies when formatting a single file).
  - `debug` :(Optional) If True, print debug information.  Defaults to False

  >To format all .jac files from walking through current located directory:
  >```bash
  >$ jac format .
  >```



## `jac check`
The `check` command is utilized to run type checker for a specified .jac file.
```bash
jac check <file_path>
```
Parameters to execute the check command:
- `file_path`: Path of .jac file to run type checker.



## `jac build`

The `build` command is utilized to build the specified .jac file.
```bash
jac build <file_path>
```
  Parameters to execute the build command:
  - `file_path`: Path of .jac file to build.



## `jac enter`

The `enter` command is utilized to run the specified entrypoint function in the given .jac file.

```bash
jac enter <file_path> <entrypoint> <args>
```
Parameters to execute the enter command:
- `file_path`: The path to the .jac file.
- `entrypoint`: The name of the entrypoint function.
- `args`: Arguments to pass to the entrypoint function.

- To enter file_path Jac file
```bash
jac enter <file_path>
```



## `jac test`

The `test` command is utilized to run the test suite in the specified .jac file.
```bash
jac test <file_path>
```
Parameters to execute the test command:
- `file_path`: The path to the .jac file.
