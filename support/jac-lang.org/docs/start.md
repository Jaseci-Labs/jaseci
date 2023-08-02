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

- To simply load a sample Jac module and exit, run:
    ```bash
    jac load -f sample.jac
    ```

- To load a sample Jac module and execute a particular function (considered the entrypoint for execution in Jac), run:
    ```bash
    jac run -f sample.jac -e my_func
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