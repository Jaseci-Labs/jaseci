"""Utility functions and classes for Jac compilation toolchain."""
import re
import textwrap


import jaclang.jac.absyntree as ast


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string


def add_line_numbers(s: str) -> str:
    """Add line numbers to a string."""
    lines = s.split("\n")
    return "\n".join(f"{i + 1}: \t{line}" for i, line in enumerate(lines))


def clip_code_section(s: str, target_line: int, line_range: int) -> str:
    """Clip a section of code and highlight target line."""
    lines = s.split("\n")
    start = max(0, target_line - line_range - 1)
    end = min(target_line + line_range, len(lines))

    result = []
    for i in range(start, end):
        line = lines[i]
        if i == target_line - 1:
            line = "*" + line
        result.append(line)
    return "\n".join(result)


def dedent_code_block(code: str) -> str:
    """Dedent a code block."""
    # lines = code.splitlines()
    # min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    # dedented_lines = [line[min_indent:] for line in lines]
    # dedented_code = "\n".join(dedented_lines)
    return textwrap.dedent(code)


def get_ast_nodes_as_snake_case() -> list[str]:
    """Get all AST nodes as snake case."""
    import inspect
    import sys

    module_name = ast.__name__
    module = sys.modules[module_name]

    # Retrieve the source code of the module
    source_code = inspect.getsource(module)

    classes = inspect.getmembers(module, inspect.isclass)
    ast_node_classes = [cls for _, cls in classes if issubclass(cls, ast.AstNode)]

    ordered_classes = sorted(
        ast_node_classes, key=lambda cls: source_code.find(f"class {cls.__name__}")
    )
    snake_names = []
    for cls in ordered_classes:
        class_name = cls.__name__
        snake_names.append(pascal_to_snake(class_name))
    return snake_names
