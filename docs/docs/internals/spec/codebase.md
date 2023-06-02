---
sidebar_position: 2
description: Codebase Guidelines and Architecture
title: Codebase Guide
---

# Codebase Guide

## General Setup and Information

The Jaseci codebase enforces the black code formatting using the black tool. It is designed to automatically format Python code according to a set of predefined style guidelines. Black enforces a consistent and opinionated code style, minimizing debates over formatting choices and promoting readability. This helps maintain a clean and uniform codebase, improving code quality and reducing the time spent on manual code formatting.

To install:
```bash
# Install black
pip3 install black
```

Our repo uses pre-commit, an open-source tool used for managing and enforcing pre-commit checks in Git repositories. Pre-commit allows us to automate the execution of code checks, ensuring code quality and reducing the likelihood of introducing bugs. It enforces consistent coding standards and style guidelines across the project, fostering better collaboration and maintainability. By catching issues before they are committed, it saves time and effort in the long run by preventing the need for manual bug fixing and code cleanup.

Once you checked out the repo, you should run
```bash
# Install pre-commit
pip3 install pre-commit
pre-commit install
```

> Note
>
> You'll need to add `--max-line-length=120 --extend-ignore=E203` arguments to `flake8` for linting. We recommend setting it up in your preferred code editor or IDE, e.g. VSCode.

Be sure to install the pytest framework and run a test to make sure everything is good to go!

First install pytest with
```shell
pip3 install pytest pytest-xdist pytest-cov
```

Then run the tests!
```shell
pytest
```

## Linting Policy

The linting process for Jaseci ensures code quality, consistency, and readability. We utilize Flake8 as the primary linter, along with the following plugins: flake8_import_order, flake8_docstrings, flake8_comprehensions, flake8_bugbear, flake8_annotations, and pep8-naming. These plugins enhance code quality and adherence to best practices.

Flake8 is a popular Python linter that combines multiple individual tools to analyze Python code. It checks for style violations, potential bugs, and adheres to the Python Enhancement Proposals (PEP) guidelines.

### Plugin Rationale

#### flake8_import_order
The flake8_import_order plugin enforces a consistent import order within Python modules, aiding readability and maintainability. It ensures that imports are organized in a standardized manner, making it easier to locate and understand module dependencies.

#### flake8_docstrings
The flake8_docstrings plugin enforces consistent and descriptive documentation strings (docstrings) for Python functions, classes, and modules. Well-documented code improves readability, facilitates understanding, and promotes code reuse. This plugin ensures adherence to standard docstring conventions, making the codebase more maintainable and accessible.

#### flake8_comprehensions
The flake8_comprehensions plugin enforces best practices when using list comprehensions, dictionary comprehensions, and generator expressions in Python. It promotes readable and concise code while avoiding unnecessary complexity. By adhering to the plugin's suggestions, developers can write efficient and understandable code.

#### flake8_bugbear
The flake8_bugbear plugin extends the capabilities of Flake8 by providing additional checks for common programming errors and code smells. It detects potential bugs and suggests improvements based on common pitfalls. The plugin helps catch subtle mistakes that could lead to runtime errors or suboptimal code.

#### flake8_annotations
The flake8_annotations plugin encourages consistent and appropriate usage of type annotations in Python code. It ensures that functions, variables, and parameters are properly annotated, improving code clarity and reducing the chances of type-related errors. Enforcing type annotations contributes to maintainable and robust codebases.

#### pep8-naming
The pep8-naming plugin enforces naming conventions specified in PEP8 for variables, functions, classes, and modules. It maintains consistency and readability across the codebase. By adhering to standard naming conventions, the code becomes more intuitive, allowing future contributors to quickly understand and navigate the project.

### Configuration and Integration

#### Installation
To apply the linting policy with the specified plugins, follow these steps:

1. Install Flake8 and the additional plugins using the following command:
```shell
pip3 install flake8 flake8-import-order flake8-docstrings flake8-comprehensions flake8-bugbear flake8-annotations pep8-naming
```

#### Configuration File
2. Create a `.flake8` configuration file in the root directory of your project with the following contents:
```ini
[flake8]
ignore = E501
exclude = .git, __pycache__, .venv
plugins = flake8_import_order, flake8_docstrings, flake8_comprehensions, flake8_bugbear, flake8_annotations, pep8-naming
```

## Codebase Organization

### Folder structure
| Folder                   | Description                                     |
|--------------------------|-------------------------------------------------|
| `/`                      | Base directory for project, organized with `setup.py` to create Jaseci pip3 package. |
| `/docs`                  | Docusaurus documentation for Jaseci.            |
| `/scripts`               | General utility scripts.                        |
| `/jaseci`                | Source code for the project.                     |
| `/jaseci/core`           | Core primitives for realizing Jaseci abstractions. |
| `/jaseci/jac`            | Language transpilation tools.                   |


### Notes

- Jac code targets parse tree that is then consumed to generate pure python as an "IR"
- Runtime is realized through the implementation of core primitives
- Element serves as an abstract class to everything in jaseci and makes it all persistable
- Objects have a context and Node, Edge, and Walker inherit it
- Protobufs is used to automatically serialize and deserialzie jaseci objects
- transpile rules should always have a 1 to 1 mapping to parser rules
- The data spacial concept is enhanced in that objects are introduced that are essentially untetherd nodes, (traditional objects), and walkers can travel to them just like notes, this walker/object dynamic is essentially a method call dynamic except paramters are in the walker through the here/visitor semantic
