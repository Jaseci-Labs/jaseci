# Getting Started with the Jac Programming Language

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

- To simply load a sample Jac module and exit, run:
    ```bash
    jac load -f sample.jac
    ```

- To load a sample Jac module and execute a particular function (considered the entrypoint for execution in Jac), run:
    ```bash
    jac run -f sample.jac -e my_func
    ```

Now Try it with this example jac program with both load and calling `test_run`

```jac
"""Example of simple walker walking nodes."""

node item {
    has value: int;
}

walker Creator {
    has count: int = 0;
    can create with root|:n:item entry {
        here ++> spawn :n:item;
        self.count += 1;
        if self.count < 10 {
            visit -->;
        }
    }
}

walker Walk {
    has count: int = 0;
    can skip_root with root entry { visit -->; }
    can step with :n:item entry {
        here.value = self.count;
        self.count += 1;
        visit --> else {
            f"Final Value: {here.value-1}" |> print;
            "Done walking." |> print;
            disengage;
        }
        f"Value: {here.value-1}" |> print;
    }
}

can test_run {
    spawn :w:Creator |> root;
    spawn :w:Walk |> root;
}

with entry {
    |> test_run;
}
```

## Integrating Jac into Python Modules

JacLang also provides a seamless way to import Jac into existing Python modules through library functions. Here's an example:

```python
"""CLI for jaclang."""
from jaclang import jac_purple_import as jac_import

cli = jac_import("cli")
cmds = jac_import("cmds")

cli.cmd_registry = cmds.cmd_reg  # type: ignore
```

In the above code snippet, `cli` and `cmds` are modules that are imported similar to how you'd typically import modules in Python, i.e., `import cli` or `import cmds`.

Below is a sample `cli.jac` file to provide some insight into how Jac code looks:

```jac
"""
This is the implementation of the command line interface tool for the
Jac language. It's built with the Jac language via bootstraping and
represents the first such complete Jac program.
"""

import:py inspect;
import:py argparse;
import:py cmd;
include:jac impl.cli_impl;

object Command {
    has func: callable,
        sig: inspect.Signature;

    can:private init(func: callable);
    can call(*args: list, **kwargs: dict);
}


object CommandRegistry {
    has:private registry: dict[str, Command],
             sub_parsers: argparse._SubParsersActionp;
    has:public parser: argparse.ArgumentParser;

    can init;
    can register(func: callable);
    can get(name: str) -> Command;
    can items -> dict[str, Command];
}


object CommandShell:cmd.Cmd {
    static has intro: str = "Welcome to the Jac CLI!",
               prompt: str = "jac> ";
    has cmd_reg: CommandRegistry;

    can init (cmd_reg: CommandRegistry);
    can do_exit(arg: list) -> bool;
    can default(line: str);
}

global cmd_registry = |> CommandRegistry;
can start_cli;
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
