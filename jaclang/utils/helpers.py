"""Utility functions and classes for Jac compilation toolchain."""
import re
import textwrap
import traceback


import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con, Values as Val


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


def handle_jac_error(code_string: str, e: Exception, tb: traceback.StackSummary) -> str:
    """Handle Jac Error."""
    except_line = e.end_lineno if isinstance(e, SyntaxError) else list(tb)[-1].lineno
    if not isinstance(except_line, int) or except_line == 0:
        return ""
    py_error_region = clip_code_section(
        add_line_numbers(code_string), except_line, Val.JAC_ERROR_LINE_RANGE
    )
    try:
        jac_err_line = int(code_string.splitlines()[except_line - 1].split()[-1])
        mod_index = int(code_string.splitlines()[except_line - 1].split()[-2])
        mod_paths = code_string.split(Con.JAC_DEBUG_SPLITTER)[1].strip().splitlines()
        target_mod = mod_paths[mod_index]
        with open(target_mod, "r") as file:
            jac_code_string = file.read()
        jac_error_region = clip_code_section(
            add_line_numbers(jac_code_string), jac_err_line, Val.JAC_ERROR_LINE_RANGE
        )
        target_mod = f"JacCode File: {target_mod}:{jac_err_line}"
    except Exception as e:
        jac_error_region = str(e)
        target_mod = ""
    snippet = (
        f"{Con.JAC_ERROR_PREAMBLE}\n"
        f"{target_mod}\n"
        f"JacCode Snippet:\n{jac_error_region}\n"
        f"PyCode Snippet:\n{py_error_region}\n"
    )
    return snippet


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
