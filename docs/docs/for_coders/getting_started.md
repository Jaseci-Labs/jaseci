# Getting Started

If you know python, there's near zero learning curve to get started.

# Installation

Firstly make sure that Python 3.12 or higher is installed in your environment, then simply install Jac using pip:

```bash
python -m pip install -U jaclang
```

Once you've got Jaclang installed, just give the Jac CLI a try to make sure everything's up and running smoothly.

- Start the Jac CLI:
    ```bash
    jac
    ```
- Run a .jac file
    ```bash
    jac run <file_name>.jac
- To test run a 'Hello World'Program
    ```bash
    echo "with entry { print('hello world'); }" > test.jac;
    jac run test.jac;
    rm test.jac;
    ```
> **Note**
>
> If these commands prints ```hello world``` you are good to go.

## <span style="color: orange">Supportive Jac CLI commands
</span>

- Clean cached files (recommended after each run):
    ```bash
    jac clean
    ```
- Print the data-spatial graph to a file and visualize it using [Graphviz](https://dreampuf.github.io/GraphvizOnline/):
    ```bash
    jac dot <file_name>.jac
    ```
    - Visit [https://dreampuf.github.io/GraphvizOnline/](https://dreampuf.github.io/GraphvizOnline/) to visualize the graph.

## <span style="color: orange">Installing the VS Code Extention
</span>

In addition to setting up JacLang itself, you may also want to take advantage of the JacLang language extension for Visual Studio Code (VSCode). This will give you enhanced code highlighting, autocomplete, and other useful language features within your VSCode environment.

- To install just visit the VS Code marketplace and install,
    - [Jac](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension)

<div class="grid cards" markdown>

-   __A Real World Example__

    ---

    *See somthing real in Jac*

    <!-- [:octicons-arrow-right-24: Getting started](#) -->

    [Little X](installation.md){ .md-button }

-   __Experience Jac in Browser__

    ---

    *Hit the Playground *

    [Jac Playground](jac_in_a_flash.md){ .md-button .md-button--primary }

</div>

## <span style="color: orange">Features in Jac-Lang</span>

While Python is widely regarded for its simplicity and versatility, jac lang offers several advantages, particularly in terms of readability, flexibility, and type safety. By addressing some of the shortcomings of Python, jac lang provides developers with a more robust and scalable alternative for building modern applications.

<!-- - Full-stack programming language
    - Jaclang empowers developers to create both front-end and back-end components of their applications using a single language. This eliminates the need to switch between different programming languages and frameworks, resulting in a more cohesive and efficient development experience. -->

- **Supersets Python**
    - As TypeScript supersets JavaScript, Jac-Lang is a language which was built on top of python which all pythony goodness available to all jac-lang programmers while including the entire python ecosystem, available to use.

- **Offers more readable code**
    - By adopting a clean and intuitive syntax, Jac Lang makes it easier for developers and coders to write code that is easy to understand and maintain.

- **More flexible than python, in terms of styling the code**
    - As jac lang uses syntax where multiline comments, multiline function declerations and more, which allows the user to arrange arguments, lists, dictionaties and other list-like objects in a readable format.

- **Type safe to support large codebases**
    - Jac lang prioritizes type safety to support the development of large-scale applications. By enforcing strict type checking, jac lang helps identify potential errors at compile time, rather than runtime, leading to more robust and reliable code.

- **Data Spatial Programming**
    - Jac Lang's programming approach focuses on data-spatial constructs, enhancing the handling and visualization of data in ways traditional programming paradigms might not support.

- **Programming with Large Language Models**
    - Jac-lang has an up & coming feature which allows programmers to integrate LLMs into their programming pipeline seamlessly without the need for learning extensive libraries and complicated new syntaxes.
<!-- ## Integrating Jac into Python Modules

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

That's all you need to get started with JacLang. As you delve into this new language, you'll discover how it beautifully combines the power of Python with a modern and intuitive syntax. Happy coding! -->