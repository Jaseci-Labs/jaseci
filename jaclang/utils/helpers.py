"""Utility functions and classes for Jac compilation toolchain."""
import re

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer


def get_all_jac_keywords() -> str:
    """Get all Jac keywords as an or string."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string


def add_line_numbers(s: str) -> str:
    """Add line numbers to a string."""
    lines = s.split("\n")
    return "\n".join(f"{i+1}: \t{line}" for i, line in enumerate(lines))


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


def load_ast_and_print_pass_template() -> str:
    """Load and print classes."""
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
    output = ""
    for cls in ordered_classes:
        class_name = cls.__name__
        snake_case_name = pascal_to_snake(class_name)

        output += f"def exit_{snake_case_name}(self, node: ast.{class_name}) -> None:\n"
        output += '    """Sub objects.\n\n'

        init_func = cls.__init__
        init_signature = inspect.signature(init_func)

        for param_name, param in init_signature.parameters.items():
            if param_name not in ["self", "parent", "kid", "line"]:
                param_type = (
                    param.annotation
                    if param.annotation != inspect.Parameter.empty
                    else "Any"
                )
                param_default = (
                    param.default if param.default != inspect.Parameter.empty else None
                )
                output += f"    {param_name}: {param_type}{' ='+param_default if param_default else ''},\n"

        output += '    """\n\n'
    output = output.replace("jaclang.jac.absyntree.", "")
    output = output.replace("typing.", "")
    output = output.replace("<enum '", "")
    output = output.replace("'>", "")
    output = output.replace("<class '", "")
    output = output.replace("ForwardRef('", "")
    output = output.replace("')", "")
    return output


if __name__ == "__main__":
    print(get_all_jac_keywords())
    print(load_ast_and_print_pass_template())
