# Jac Extension

This extension provides support for the [Jac](https://doc.jaseci.org) programming language. It provides syntax highlighting and leverages the LSP to provide a rich editing experience.

# Quick Start

When you install the extension you will need to add a setting to your `settings.json` file that points to the python path of your Jaseci environment.

1. Activate your python environment where for which Jaseci is installed.
2. Create a `.vscode/settings.json` file in your project root if one is not already present.
3. Go to your terminal and run `which python` and copy the path.
4. Update your `settings.json` file in the `.vscode` directory by adding `jac.pythonPath` to the settings object with the path you copied.

Example:

```json
{
  "jac.pythonPath": "/Users/john_doe/mambaforge/envs/jac/bin/python"
}
```

# Features

- Code completion
- Syntax highlighting
- Snippets
- Go to definition
- Document symbols, workspace symbols
- Variables hint, and documentation on hover
- Diagnostics

# Contributing

## Install Server Dependencies

1. `python -m venv env`
2. `python -m pip install -e .` from root directory
3. Create `.vscode/settings.json` file and set `jac.pythonPath` to point to your python environment where `jaseci` is installed

## Install Client Dependencies

Open terminal and execute following commands:

1. `yarn install`
1. `cd client/ && yarn install`

## Run Extension

1. Open this directory in VS Code
2. Open debug view (`ctrl + shift + D`)
3. Select `Server + Client` and press `F5`
