# Contrib and Codebase Guide

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

> Important
>
> If you are making changes / updates to the main transpiler/compiler you may want to periodically run `jac clean` and/or `source scripts/clean_jac_gen.sh` to clean any cached bytecode of the bootstrapped transpiler. (otherwise you may be running stale cached implementations of the `jac` tool.)

## Linting Policy

The linting process for Jaseci ensures code quality, consistency, and readability. We utilize Flake8 as the primary linter, along with the following plugins: flake8_import_order, flake8_docstrings, flake8_comprehensions, flake8_bugbear, flake8_annotations, and pep8-naming. These plugins enhance code quality and adherence to best practices.

Flake8 is a popular Python linter that combines multiple individual tools to analyze Python code. It checks for style violations, potential bugs, and adheres to the Python Enhancement Proposals (PEP) guidelines.

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

### Plugin Description and Rationale

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

## Commiting Code

### Conventional Commits Policy for Jac

For Jac, we (now) adhere to the Conventional Commits specification to ensure our commit history is readable and understandable. This helps in generating changelogs and eases the process of versioning. Below is a guide to understanding and implementing Conventional Commits in your contributions to Jac.

### Commit Message Format

Each commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples of Commits

1. **feat**: Introduction of new features or syntax to the language
    - Example: `feat(syntax): add pattern matching capabilities similar based on match from Python 3.10`
2. **fix**: Correction of bugs or inconsistencies in the language's implementation or its standard library
    - Example: `fix(runtime): resolve memory leak issue in list comprehensions`
3. **docs**: Updates or improvements to documentation, including both in-code and external docs
    - Example: `docs(guide): add examples for async functionality in tutorial section`
4. **style**: Code changes that improve readability or conform to style guidelines without altering behavior
    - Example: `style(compiler): refactor parser for better readability`
5. **refactor**: Code changes that neither fix a bug nor add a feature but improve structure or design
    - Example: `refactor(core): modularize interpreter to simplify future extensions`
6. **perf**: Enhancements that significantly improve performance of the language or its runtime
    - Example: `perf(jit): optimize just-in-time compilation for recursive functions`
7. **test**: Addition or correction of tests for the language's features or standard library
    - Example: `test(standard-lib): increase test coverage for the datetime module`
8. **chore**: Routine tasks such as updating build scripts, dependencies, etc.
    - Example: `chore(build): update dependencies to latest versions`
9. **build**: Changes that affect the build system, compiler, or other infrastructural components
    - Example: `build(compiler): upgrade LLVM backend to support new optimizations`
10. **ci**: Modifications to the Continuous Integration setup, affecting how builds and tests are run
    - Example: `ci(pipeline): add linting stage to the CI pipeline`

### Scope

The scope should be a specific module or aspect of the language or its ecosystem, like `syntax`, `runtime`, `standard-lib`, `compiler`, etc.

### Description

The description concisely summarizes the change, focusing on why it is necessary rather than how it is implemented.

### Optional Body and Footer

The body provides more context, explaining the rationale behind the change and contrasting it with previous behavior.

The footer is used for indicating any breaking changes and linking to relevant GitHub issues or discussions.

### Full Examples

Here are some detailed examples relevant that uses body and footers:

- **Feature Commit**:
  ```
  feat(concurrency): introduce async-await syntax for improved concurrency support

  This feature aligns Jac with modern concurrency practices, allowing for more efficient and readable asynchronous code.

  Part of #789
  ```

- **Bug Fix Commit**:
  ```
  fix(type-checking): correct type inference for nested functions

  This fix addresses a critical issue where the type checker incorrectly inferred types for nested functions, leading to runtime errors.

  Resolves #456
  ```

By adhering to these guidelines, your contributions will greatly assist in the systematic development and maintenance of Jac. We value and appreciate your commitment to enhancing this language!