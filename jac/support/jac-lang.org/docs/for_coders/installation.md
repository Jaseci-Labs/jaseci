# <span style="color: orange; font-weight: bold">Installation</span>

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