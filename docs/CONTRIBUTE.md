# Contributing to MTLLM Documentation

<!-- ## How to find, add and change the documentation architecture

When adding content to the documentations maintain the document structure used in [docs](./docs/) folder. To include a new file or content into the documentation, edit the [mkdocs.yml](./mkdocs.yml) file.

As an example consider adding a new 'example.md' file residing in file path './docs/learn' in to the [mkdocs.yml](./mkdocs.yml) file, under the 'for_contributors' subsection. The file should change as following.

```yaml
...
nav:
    ...
    - ~/learn$:
      ...
      - ~/for_contributors:
        ...
        - 'learn/example.md'
      ...
...
``` -->

## Running a local preview instance of the documentation

To open a preview of the codedoc server locally, following steps should be followed.



1. Make sure Node.js is properly installed on your linux system.

    ```bash
    curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ```

2. install codedoc cli and required packages.

    ```bash
    npm i -g @codedoc/cli
    codedoc install
    ```
4. Initiate the codedoc server within ```docs\```

    ```bash
    codedoc serve
    ```

3. When prompted open the server from a web browser or the VS Code editor itself.

    >    Default - http://localhost:3000/mtllm 