# Getting Started with JacLang

Welcome to JacLang, a unique and powerful programming language that runs on top of Python. To get you started, this guide will walk you through the process of installation, running Jac files, and importing Jac into existing Python modules.

## Installation

<div class="grid cards" markdown>

-   __Setup in a nutshell__

    ---

    *To get you started working with Jac Lang, this guide will walk you through the process of installation, running Jac files, and importing Jac into existing Python modules.*

    <!-- [:octicons-arrow-right-24: Getting started](#) -->

    [Setup Now](start/installation.md){ .md-button }

-   __Jac in a FLASH__

    ---

    *If you are already a fluent pythonista jump into learning by going through a step-by-step transformation from python to jac-lang and BEYOND!*

    [Get Started](start/jac_in_a_flash.md){ .md-button .md-button--primary }

</div>

Firstly, you'll need to install JacLang. You can do this easily through Python's package manager, pip. Run the following command:

```bash
pip install jaclang
```

And from source simply use,

```bash
pip install -e .
```

Upon successful installation, you'll have a script named `jac` at your disposal. This script is used to load and run `.jac` files.

## Running Jac Files

Here's how you can use `jac`:

- To simply run a Jac program file, run:
    ```bash
    jac run sample.jac
    ```

- To load a Jac module and execute a particular function (considered the entrypoint for execution in Jac), run:
    ```bash
    jac enter sample.jac -e my_func
    ```

Now Try it with this example jac program:

=== "guess_game.py"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game.py"
    ```
=== "guess_game1.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game1.jac"
    ```
=== "guess_game2.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game2.jac"
    ```
=== "guess_game3.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game3.jac"
    ```
=== "guess_game4.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game4.jac"
    ```
=== "guess_game5.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game5.jac"
    ```

## Integrating Jac into Python Modules

JacLang also provides a seamless way to import Jac into existing Python modules through library functions. Here's an example:

```python
"""CLI for jaclang."""
from jaclang import jac_import

cli = jac_import("cli")
cmds = jac_import("cmds")

cli.cmd_registry = cmds.cmd_reg  # type: ignore
```

In the above code snippet, `cli` and `cmds` are modules that are imported similar to how you'd typically import modules in Python, i.e., `import cli` or `import cmds`.

Below is the actual implementation for Jac's CLI (`cli.jac`) to provide some insight into how Jac code looks:

=== "cli.jac"
    ```jac linenums="1"
    --8<-- "jaclang/cli/cli.jac"
    ```
=== "cli_impl.jac"
    ```jac linenums="1"
    --8<-- "jaclang/cli/cli_impl.jac"
    ```

That's all you need to get started with JacLang. As you delve into this new language, you'll discover how it beautifully combines the power of Python with a modern and intuitive syntax. Happy coding!

## Installing JacLang Extension in Visual Studio Code (VSCode)

In addition to setting up JacLang itself, you may also want to take advantage of the JacLang language extension for Visual Studio Code (VSCode). This will give you enhanced code highlighting, autocomplete, and other useful language features within your VSCode environment.

Here's a step-by-step guide on how to package and install the JacLang VSCode extension.