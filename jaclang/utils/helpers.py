"""Utility functions and classes for Jac compilation toolchain."""

import dis
import marshal
import os
import pdb
import re


import jaclang.compiler.absyntree as ast


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string


def heading_to_snake(heading: str) -> str:
    """Convert string to snakecase including replacing(/ ,- )."""
    return heading.strip().replace("-", "_").replace("/", "_").replace(" ", "_").lower()


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


def extract_headings(file_path: str) -> dict[str, tuple[int, int]]:
    """Extract headings of contetnts in Jac grammer."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    headings = {}
    current_heading = None
    start_line = 0
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("//"):
            if current_heading is not None:
                headings[current_heading] = (
                    start_line,
                    idx - 2,
                )  # Subtract 1 to get the correct end line
            current_heading = line.strip()[2:]
            start_line = idx + 1
    # Add the last heading
    if current_heading is not None:
        headings[current_heading] = (start_line, len(lines))
    return headings


def import_target_to_relative_path(
    import_target: str, base_path: str | None = None, file_extension: str = ".jac"
) -> str:
    """Convert an import target string into a relative file path."""
    if base_path is None:
        base_path = os.getcwd()
    parts = import_target.split(".")
    traversal_levels = 0
    for part in parts:
        if part == "":
            traversal_levels += 1
        else:
            break  # Stop at the first non-empty part
    traversal_levels = traversal_levels - 1 if traversal_levels > 0 else 0
    actual_parts = parts[traversal_levels:]
    for _ in range(traversal_levels):
        base_path = os.path.dirname(base_path)
    relative_path = os.path.join(base_path, *actual_parts) + file_extension
    return relative_path


class Jdb(pdb.Pdb):
    """Jac debugger."""

    def __init__(self, *args, **kwargs) -> None:  # noqa
        """Initialize the Jac debugger."""
        super().__init__(*args, **kwargs)
        self.prompt = "Jdb > "

    def has_breakpoint(self, bytecode: bytes) -> bool:
        """Check for breakpoint."""
        code = marshal.loads(bytecode)
        instructions = dis.get_instructions(code)
        return any(
            instruction.opname in ("LOAD_GLOBAL", "LOAD_NAME", "LOAD_FAST")
            and instruction.argval == "breakpoint"
            for instruction in instructions
        )


debugger = Jdb()
