"""Utility functions and classes for Jac compilation toolchain."""

import dis
import marshal
import os
import pdb
import re
from traceback import TracebackException


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
            f'## {heading}\n**Code Example**\n=== "Jac"\n    ```jac linenums="1"\n    --8<-- "examples/reference/'
            f'{heading_snakecase}.jac"\n'
            f'    ```\n=== "Python"\n    ```python linenums="1"\n    --8<-- "examples/reference/'
            f'{heading_snakecase}.py"\n    ```\n'
            f'??? example "Jac Grammar Snippet"\n    ```yaml linenums="{lines[0]}"\n    --8<-- '
            f'"jaclang/compiler/jac.lark:{lines[0]}:{lines[1]}"\n    ```\n'
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


def is_standard_lib_module(module_path: str) -> bool:
    """Check if a module is a standard library module."""
    import os
    import sysconfig

    stdlib_dir = sysconfig.get_paths()["stdlib"]
    direc_path = os.path.join(stdlib_dir, module_path)
    file_path = direc_path + ".py"
    return os.path.isfile(file_path) or os.path.isdir(direc_path)


def dump_traceback(e: Exception) -> str:
    """Dump the stack frames of the exception."""
    trace_dump = ""

    # Utility function to get the error line char offset.
    def byte_offset_to_char_offset(string: str, offset: int) -> int:
        return len(string.encode("utf-8")[:offset].decode("utf-8", errors="replace"))

    tb = TracebackException(type(e), e, e.__traceback__, limit=None, compact=True)
    trace_dump += f"Error: {str(e)}\n"

    # The first frame is the call the to the above `exec` function, not usefull to the enduser,
    # and Make the most recent call first.
    tb.stack.pop(0)
    tb.stack.reverse()

    # FIXME: should be some settings, we should replace to ensure the anchors length match.
    dump_tab_width = 2

    for idx, frame in enumerate(tb.stack):
        func_signature = frame.name + ("()" if frame.name.isidentifier() else "")

        # Pretty print the most recent call's location.
        if idx == 0 and (
            (frame.lineno is not None) and frame.line and frame.line.strip() != ""
        ):

            line_o = frame._original_line.rstrip()  # type: ignore [attr-defined]
            if frame.colno is not None and frame.end_colno is not None:
                off_start = byte_offset_to_char_offset(line_o, frame.colno) - 1
                off_end = byte_offset_to_char_offset(line_o, frame.end_colno) - 1

                # Get the source.
                file_source = None
                with open(frame.filename, "r") as file:
                    file_source = file.read()

                # Get the source offset.
                lines = file_source.split("\n")
                for i in range(frame.lineno - 1):
                    off_start += len(lines[i]) + 1
                    off_end += len(lines[i]) + 1

                trace_dump += pretty_print_source_location(
                    frame.filename, file_source, frame.lineno, off_start, off_end
                )

        trace_dump += f'\n{" " * dump_tab_width}at {func_signature} {frame.filename}:{frame.lineno}'

    return trace_dump


# TODO: After implementing the TextRange (or simillar named) class to mark a text range
# refactor the parameter to accept an instace of that text range object.
def pretty_print_source_location(
    file_path: str,
    file_source: str,
    error_line: int,
    pos_start: int,
    pos_end: int,
) -> str:
    """Pretty print internal method for the pretty_print method."""
    # NOTE: The Line numbers and the column numbers are starts with 1.
    # We print totally 5 lines (error line and above 2 and bellow 2).

    # The width of the line number we'll be printing (more of a settings).
    line_num_width: int = 5

    idx: int = pos_start  # Pointer for the current character.

    if file_source == "" or file_path == "":
        return ""

    start_line: int = error_line - 2
    if start_line < 1:
        start_line = 1
    end_line: int = start_line + 5  # Index is exclusive.

    # Get the first character of the [start_line].
    file_source.splitlines(True)[start_line - 1]
    curr_line: int = error_line
    while idx >= 0 and curr_line >= start_line:
        idx -= 1
        if idx < 0:
            break
        if file_source[idx] == "\n":
            curr_line -= 1

    idx += 1  # Enter the line.
    assert idx == 0 or file_source[idx - 1] == "\n"

    pretty_dump = ""

    # Print each lines.
    curr_line = start_line
    while curr_line < end_line:
        pretty_dump += f"%{line_num_width}d | " % curr_line

        idx_line_start = idx
        while idx < len(file_source) and file_source[idx] != "\n":
            idx += 1  # Run to the line end.
        pretty_dump += file_source[idx_line_start:idx]
        pretty_dump += "\n"

        if curr_line == error_line:  # Print the current line with indicator.
            pretty_dump += f"%{line_num_width}s | " % " "

            spaces = ""
            for idx_pre in range(idx_line_start, pos_start):
                spaces += "\t" if file_source[idx_pre] == "\t" else " "

            err_token_len = pos_end - pos_start
            pretty_dump += spaces + ("^" * err_token_len) + "\n"

        if idx == len(file_source):
            break
        curr_line += 1
        idx += 1

    return pretty_dump[:-1]  # Get rid of the last newline (of the last line).


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
