# Contrib and Codebase Guide

## General Setup and Information

To get setup run
```bash
# Install black
pip3 install pre-commit
pre-commit install
```

To understand our linting and mypy type checking have a look at our pre-commit actions. You can set up your enviornment accordingly. For help interpreting this if you need it, call upon our friend Mr. ChatGPT or one of his colleagues.

??? Grock "Our pre-commit process"
    ```yaml linenums="1"
    --8<-- ".pre-commit-config.yaml"
    ```

This is how we run checks on demand.

```bash
--8<-- "scripts/check.sh"
```

This is how we run our tests.

```bash
--8<-- "scripts/tests.sh"
```

## Run docs site locally

This is how we run the docs

```bash
--8<-- "scripts/run_docs.sh"
```

This is how we kill the docs if it dies for some reason
```bash
--8<-- "scripts/kill_docs.sh"
```


## Build VSCode Extention

```bash
--8<-- "scripts/build_vsce.sh"
```

