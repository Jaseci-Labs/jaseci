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
pip install black
```

Our repo uses pre-commit, an open-source tool used for managing and enforcing pre-commit checks in Git repositories. Pre-commit allows us to automate the execution of code checks, ensuring code quality and reducing the likelihood of introducing bugs. It enforces consistent coding standards and style guidelines across the project, fostering better collaboration and maintainability. By catching issues before they are committed, it saves time and effort in the long run by preventing the need for manual bug fixing and code cleanup.

Once you checked out the repo, you should run
```bash
# Install pre-commit
pip install pre-commit
pre-commit install
```

> Note
>
> You'll need to add `--max-line-length=88 --extend-ignore=E203` arguments to `flake8` for linting. We recommend setting it up in your preferred code editor or IDE, e.g. VSCode.