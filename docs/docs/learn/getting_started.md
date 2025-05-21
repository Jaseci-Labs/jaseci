<h1 style="color: orange; font-weight: bold; text-align: center;">Getting Started With Jac and Jaseci</h1>

Jac is an innovative programming language that extends Python's semantics while maintaining full interoperability with the Python ecosystem. It introduces cutting-edge programming models and abstractions specifically designed to minimize and hide complexity, embrace AI-forward development, and automate categories of common software systems that typically require manual implementation. Despite being relatively new, Jac has already proven its production-grade capabilities, currently powering several real-world applications across various use cases.

Jaseci serves as the implementation of the Jac runtime, functioning in a relationship similar to how CPython serves as the reference implementation for Python. This runtime environment enables Jac code to execute with its enhanced features while maintaining the seamless Python interoperability that makes the language particularly accessible to Python developers.

# Installation

Firstly make sure that Python 3.12 or higher is installed in your environment, then simply install Jac using pip:

```bash
python -m pip install -U jaclang
```

Once you've got Jaclang installed, just give the Jac CLI a try to make sure everything's up and running smoothly.

- Start the Jac CLI:
    ```bash
    jac --version
    ```
- Run a .jac fil
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

## <span style="color: orange">Installing the VS Code Extention
</span>

In addition to setting up JacLang itself, you may also want to take advantage of the JacLang language extension for Visual Studio Code (VSCode). This will give you enhanced code highlighting, autocomplete, and other useful language features within your VSCode environment.

- To install just visit the VS Code marketplace and install,
    - [Jac](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension)

## Next Steps

<div class="grid cards" markdown>

-   __Jac in a Flash__

    ---

    *See Jac's Syntax with a Toy*

    [Jac in a Flash](jac_in_a_flash.md){ .md-button .md-button--primary }

-   __A Real World Example__

    ---

    *See somthing real in Jac*

    <!-- [:octicons-arrow-right-24: Getting started](#) -->

    [A Robust Example](examples/littleX/overview.md){ .md-button }

-   __Experience Jac in Browser__

    ---

    *Hit the Playground*

    [Jac Playground](../../playground){ .md-button .md-button--primary }

</div>

