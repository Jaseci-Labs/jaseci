# Getting Started with JacLang

Welcome to JacLang, a unique and powerful programming language that runs on top of Python. To get you started, this guide will walk you through the process of installation, running Jac files, and importing Jac into existing Python modules.

## Installation

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

=== "guess_game.jac"
    ```jac linenums="1"
    --8<-- "examples/guess_game/guess_game4.jac"
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

### Setting Up VSCE

To create the VSIX file for the extension, you'll need `vsce`, a command-line tool for packaging VSCode extensions. If you don't have it installed already, follow these steps:

1. Ensure that you have Node.js (>= 0.10.x) and npm installed on your machine.

2. Open a terminal (or command prompt) and install `vsce` globally by running the following command:

    ```bash
    npm install -g vsce
    ```

### Packaging the Extension

Once you have `vsce` set up, navigate to the JacLang extension directory in your local JacLang repository by running:

```bash
cd /path/to/repo/jaclang/support/vscode_ext/jac
```

In the `jac` directory, package the extension into a VSIX file by running:

```bash
vsce package
```

This will create a `.vsix` file, which is the packaged extension.

### Installing the VSIX File in VSCode

To install the packaged JacLang extension in VSCode:

1. Open Visual Studio Code.

2. Click on the Extensions view icon on the Sidebar (or press `Ctrl+Shift+X`).

3. Click on the three-dot menu (`...`) in the top-right corner of the Extensions view.

4. Select `Install from VSIX...` from the dropdown menu.

5. In the file picker, find and select the `.vsix` file you created earlier and click `Open`.

6. After a brief moment, the extension will be installed. You might have to reload VSCode for the changes to take effect.

Now, you're all set to use the JacLang language extension in your VSCode editor! Enjoy your enhanced JacLang development experience.
