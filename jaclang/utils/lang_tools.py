"""Language tools for the Jaclang project."""

import ast as py_ast
import inspect
import os
import sys
from typing import List, Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.compile import jac_file_to_pass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.compiler.symtable import SymbolTable
from jaclang.utils.helpers import extract_headings, heading_to_snake, pascal_to_snake


class AstKidInfo:
    """Information about a kid."""

    def __init__(self, name: str, typ: str, default: Optional[str] = None) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.default = default


class AstNodeInfo:
    """Meta data about AST nodes."""

    type_map: dict[str, type] = {}

    def __init__(self, cls: type) -> None:
        """Initialize."""
        self.cls = cls
        self.process(cls)

    def process(self, cls: Type[ast.AstNode]) -> None:
        """Process AstNode class."""
        self.name = cls.__name__
        self.doc = cls.__doc__
        AstNodeInfo.type_map[self.name] = cls
        self.class_name_snake = pascal_to_snake(cls.__name__)
        self.init_sig = inspect.signature(cls.__init__)
        self.kids: list[AstKidInfo] = []
        for param_name, param in self.init_sig.parameters.items():
            if param_name not in [
                "self",
                "parent",
                "kid",
                "line",
                "sym_tab",
            ]:
                param_type = (
                    param.annotation
                    if param.annotation != inspect.Parameter.empty
                    else "Any"
                )
                param_default = (
                    param.default if param.default != inspect.Parameter.empty else None
                )
                self.kids.append(AstKidInfo(param_name, param_type, param_default))


class AstTool:
    """Ast tools."""

    def __init__(self) -> None:
        """Initialize."""
        module = sys.modules[ast.__name__]
        source_code = inspect.getsource(module)
        classes = inspect.getmembers(module, inspect.isclass)
        ast_node_classes = [
            AstNodeInfo(cls)
            for _, cls in classes
            if issubclass(cls, ast.AstNode)
            and cls.__name__
            not in [
                "AstNode",
                "OOPAccessNode",
                "WalkerStmtOnlyNode",
                "JacSource",
                "EmptyToken",
                "AstSymbolNode",
                "AstAccessNode",
                "TokenSymbol",
                "Literal",
                "AstDocNode",
                "AstSemStrNode",
                "PythonModuleAst",
                "AstAsyncNode",
                "AstElseBodyNode",
                "AstTypedVarNode",
                "AstImplOnlyNode",
                "Expr",
                "AtomExpr",
                "ElementStmt",
                "ArchBlockStmt",
                "EnumBlockStmt",
                "CodeBlockStmt",
                "NameSpec",
                "ArchSpec",
                "MatchPattern",
            ]
        ]

        self.ast_classes = sorted(
            ast_node_classes,
            key=lambda cls: source_code.find(f"class {cls.name}"),
        )

    def pass_template(self) -> str:
        """Generate pass template."""
        output = (
            "import jaclang.compiler.absyntree as ast\n"
            "from jaclang.compiler.passes import Pass\n\n"
            "class SomePass(Pass):\n"
        )

        def emit(to_append: str) -> None:
            """Emit to output."""
            nonlocal output
            output += "\n    " + to_append

        for cls in self.ast_classes:
            emit(
                f"def exit_{cls.class_name_snake}(self, node: ast.{cls.name}) -> None:"
            )
            emit('    """Sub objects.\n')

            for kid in cls.kids:
                emit(
                    f"    {kid.name}: {kid.typ}{' =' + str(kid.default) if kid.default else ''},"
                )

            emit('    """\n')
        output = (
            output.replace("jaclang.compiler.absyntree.", "")
            .replace("typing.", "")
            .replace("<enum '", "")
            .replace("'>", "")
            .replace("<class '", "")
            .replace("ForwardRef('", "")
            .replace("')", "")
        )
        return output

    def py_ast_nodes(self) -> str:
        """List python ast nodes."""
        from jaclang.compiler.passes.main import PyastBuildPass

        visit_methods = [
            method for method in dir(py_ast._Unparser) if method.startswith("visit_")  # type: ignore
        ]
        node_names = [method.replace("visit_", "") for method in visit_methods]
        pass_func_names = []
        for name, value in inspect.getmembers(PyastBuildPass):
            if name.startswith("proc_") and inspect.isfunction(value):
                pass_func_names.append(name.replace("proc_", ""))
        output = ""
        missing = []
        for i in node_names:
            nd = pascal_to_snake(i)
            this_func = (
                f"def proc_{nd}(self, node: py_ast.{i}) -> ast.AstNode:\n"
                + '    """Process python node."""\n\n'
            )
            if nd not in pass_func_names:
                missing.append(this_func)
            output += this_func
        for i in missing:
            output += f"# missing: \n{i}\n"
        return output

    def md_doc(self) -> str:
        """Generate mermaid markdown doc."""
        output = ""
        for cls in self.ast_classes:
            if not len(cls.kids):
                continue
            output += f"## {cls.name}\n"
            output += "```mermaid\nflowchart LR\n"
            for kid in cls.kids:
                if "_end" in kid.name:
                    kid.name = kid.name.replace("_end", "_end_")
                arrow = "-.->" if "Optional" in kid.typ else "-->"
                typ = (
                    kid.typ.replace("Optional[", "")
                    .replace("SubNodeList[", "")
                    .replace("SubTag[", "")
                    .replace("Sequence[", "")
                    .replace("]", "")
                    .replace("|", ",")
                    .replace("list[", "list - ")
                )
                output += f"{cls.name} {arrow}|{typ}| {kid.name}\n"
            output += "```\n\n"
            output += f"{cls.doc} \n\n"
        return output

    def ir(self, args: List[str]) -> str:
        """Generate a AST, SymbolTable tree for .jac file, or Python AST for .py file."""
        if len(args) != 2:
            return "Usage: ir <choose one of (sym / sym. / ast / ast. / pyast / py)> <file_path>"

        output, file_name = args

        if not os.path.isfile(file_name):
            return f"Error: {file_name} not found"

        if file_name.endswith(".jac"):
            [base, mod] = os.path.split(file_name)
            base = base if base else "./"
            ir = jac_file_to_pass(
                file_name, schedule=py_code_gen_typed
            ).ir  # Assuming jac_file_to_pass is defined elsewhere

            match output:
                case "sym":
                    return (
                        ir.sym_tab.pp()
                        if isinstance(ir.sym_tab, SymbolTable)
                        else "Sym_tab is None."
                    )
                case "sym.":
                    return (
                        ir.sym_tab.dotgen()
                        if isinstance(ir.sym_tab, SymbolTable)
                        else "Sym_tab is None."
                    )
                case "ast":
                    return ir.pp()
                case "ast.":
                    return ir.dotgen()
                case "unparse":
                    return ir.unparse()
                case "pyast":
                    return (
                        f"\n{py_ast.dump(ir.gen.py_ast[0], indent=2)}"
                        if isinstance(ir.gen.py_ast[0], py_ast.AST)
                        else "Compile failed."
                    )
                case "py":
                    return (
                        f"\n{ir.gen.py}"
                        if isinstance(ir.gen.py[0], str)
                        else "Compile failed."
                    )
                case _:
                    return "Invalid key: Use one of (sym / sym. / ast / ast. / pyast) followed by file_path."
        elif file_name.endswith(".py") and output == "pyast":
            [base, mod] = os.path.split(file_name)
            base = base if base else "./"
            with open(file_name, "r") as file:
                code = file.read()
            parsed_ast = py_ast.parse(code)
            return f"\n{py_ast.dump(parsed_ast, indent=2)}"
        else:
            return "Not a .jac or .py file, or invalid command for file type."

    def automate_ref(self) -> str:
        """Automate the reference guide generation."""
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
        return "References generated."
