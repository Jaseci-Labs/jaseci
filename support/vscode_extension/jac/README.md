# Example JSON VSCode extension with example Pygls Language Server

This is a slightly more detailed example Language Server than the Hello World one. Like Hello World, it uses LSP Completions as its central feature, but adds some long-running background work to demonstrate methods to handle asynchronicity and progress notifications.

Although we include a complete VSCode client here, you may also be interested in Microsoft's [client template for Python tools](https://github.com/microsoft/vscode-python-tools-extension-template). It is focussed on Python-related Language Server tooling, but it is specifically tailored to Pygls, so may have some unique insights.

## Install Server Dependencies

1. `python -m venv env`
1. `python -m pip install -e .` from root directory
1. Create `.vscode/settings.json` file and set `python.interpreterPath` to point to your python environment where `pygls` is installed

## Install Client Dependencies

Open terminal and execute following commands:

1. `npm install`
1. `cd client/ && npm install`

## Run Example

1. Open this directory in VS Code
1. Open debug view (`ctrl + shift + D`)
1. Select `Server + Client` and press `F5`
