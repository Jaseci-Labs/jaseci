"""Utility functions and classes for Jac compilation toolchain."""

import dis
import marshal
import os
import pdb
import re
from typing import Optional


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
    import jaclang.compiler.absyntree as ast

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


def auto_generate_refs() -> None:
    """Auto generate lang reference for docs."""
    file_path = os.path.join(
        os.path.split(os.path.dirname(__file__))[0], "../jaclang/compiler/jac.lark"
    )
    result = extract_headings(file_path)
    created_file_path = os.path.join(
        os.path.split(os.path.dirname(__file__))[0],
        "../support/jac-lang.org/docs/learn/jac_ref.md",
    )
    destination_folder = os.path.join(
        os.path.split(os.path.dirname(__file__))[0], "../examples/reference/"
    )
    with open(created_file_path, "w") as md_file:
        md_file.write(
            '# Jac Language Reference\n\n--8<-- "examples/reference/introduction.md"\n\n'
        )
    for heading, lines in result.items():
        heading = heading.strip()
        heading_snakecase = heading_to_snake(heading)
        content = (
            f'## {heading}\n**Grammar Snippet**\n```yaml linenums="{lines[0]}"\n--8<-- '
            f'"jaclang/compiler/jac.lark:{lines[0]}:{lines[1]}"\n```\n'
            f'**Code Example**\n=== "Jac"\n    ```jac linenums="1"\n    --8<-- "examples/reference/'
            f'{heading_snakecase}.jac"\n'
            f'    ```\n=== "Python"\n    ```python linenums="1"\n    --8<-- "examples/reference/'
            f'{heading_snakecase}.py"\n    ```\n'
            "**Description**\n\n--8<-- "
            f'"examples/reference/'
            f'{heading_snakecase}.md"\n'
        )
        with open(created_file_path, "a") as md_file:
            md_file.write(f"{content}\n")
        md_file_name = f"{heading_snakecase}.md"
        md_file_path = os.path.join(destination_folder, md_file_name)
        if not os.path.exists(md_file_path):
            with open(md_file_path, "w") as md_file:
                md_file.write("")


def import_target_to_relative_path(
    import_level: int,
    import_target: str,
    base_path: Optional[str] = None,
    file_extension: str = ".jac",
) -> str:
    """Convert an import target string into a relative file path."""
    if not base_path:
        base_path = os.getcwd()
    parts = import_target.split(".")
    traversal_levels = import_level - 1 if import_level > 0 else 0
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
