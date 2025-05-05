"""Language tools for the Jaclang project."""

import ast as py_ast
import inspect
import os
import sys
from typing import List, Optional, Type

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes.main import CompilerMode as CMode, PyastBuildPass
from jaclang.compiler.program import JacProgram
from jaclang.compiler.unitree import UniScopeNode
from jaclang.utils.helpers import auto_generate_refs, pascal_to_snake


class AstKidInfo:
    """Information about a kid."""

    def __init__(self, name: str, typ: str, default: Optional[str] = None) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.default = default


class UniNodeInfo:
    """Meta data about AST nodes."""

    type_map: dict[str, type] = {}

    def __init__(self, cls: type) -> None:
        """Initialize."""
        self.cls = cls
        self.process(cls)

    def process(self, cls: Type[uni.UniNode]) -> None:
        """Process UniNode class."""
        self.name = cls.__name__
        self.doc = cls.__doc__
        UniNodeInfo.type_map[self.name] = cls
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
        module = sys.modules[uni.__name__]
        source_code = inspect.getsource(module)
        classes = inspect.getmembers(module, inspect.isclass)
        uni_node_classes = [
            UniNodeInfo(cls)
            for _, cls in classes
            if issubclass(cls, uni.UniNode)
            and cls.__name__
            not in [
                "UniNode",
                "UniScopeNode",
                "ProgramModule",
                "OOPAccessNode",
                "WalkerStmtOnlyNode",
                "Source",
                "EmptyToken",
                "AstSymbolNode",
                "AstSymbolStubNode",
                "AstAccessNode",
                "Literal",
                "AstDocNode",
                "AstImplNeedingNode",
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
                "NameAtom",
                "ArchSpec",
                "MatchPattern",
            ]
        ]

        self.ast_classes = sorted(
            uni_node_classes,
            key=lambda cls: source_code.find(f"class {cls.name}"),
        )

    def pass_template(self) -> str:
        """Generate pass template."""
        output = (
            "import jaclang.compiler.unitree as ast\n"
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
            output.replace("jaclang.compiler.unitree.", "")
            .replace("typing.", "")
            .replace("<enum '", "")
            .replace("'>", "")
            .replace("<class '", "")
            .replace("ForwardRef('", "")
            .replace("')", "")
        )
        return output

    def py_uni_nodes(self) -> str:
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
                f"def proc_{nd}(self, node: py_ast.{i}) -> ast.UniNode:\n"
                + '    """Process python node."""\n\n'
            )
            if nd not in pass_func_names:
                missing.append(this_func)
            output += this_func
        for i in missing:
            output += f"# missing: \n{i}\n"
        return output

    def ir(self, args: List[str]) -> str:
        """Generate a AST, SymbolTable tree for .jac file, or Python AST for .py file."""
        error = "Usage: ir <choose one of (sym / sym. / ast / ast. / pyast / py / unparse)> <.py or .jac file_path>"
        if len(args) != 2:
            return error

        output, file_name = args
        prog = JacProgram()
        if not os.path.isfile(file_name):
            return f"Error: {file_name} not found"

        if file_name.endswith((".jac", ".py")):
            [base, mod] = os.path.split(file_name)
            base = base if base else "./"

            if file_name.endswith(".py"):
                with open(file_name, "r") as f:
                    file_source = f.read()
                    parsed_ast = py_ast.parse(file_source)
                if output == "pyast":
                    return f"\n{py_ast.dump(parsed_ast, indent=2)}"
                try:
                    rep = PyastBuildPass(
                        ir_in=uni.PythonModuleAst(
                            parsed_ast,
                            orig_src=uni.Source(file_source, file_name),
                        ),
                        prog=prog,
                    ).ir_out

                    ir = prog.compile_from_str(
                        source_str=rep.unparse(),
                        file_path=file_name[:-3] + ".jac",
                        mode=CMode.TYPECHECK,
                    )
                except Exception as e:
                    return f"Error While Jac to Py AST conversion: {e}"
            else:
                ir = prog.compile(file_name, mode=CMode.TYPECHECK)

            match output:
                case "sym":
                    out = ""
                    for module_ in prog.mod.hub.values():
                        mod_name = module_.name
                        t = "#" * len(mod_name)
                        out += f"##{t}##\n# {mod_name} #\n##{t}##\n{module_.sym_tab.sym_pp()}\n"
                    return out
                case "sym.":
                    return (
                        ir.sym_tab.sym_dotgen()
                        if isinstance(ir.sym_tab, UniScopeNode)
                        else "Sym_tab is None."
                    )
                case "ast":
                    out = ""
                    for module_ in prog.mod.hub.values():
                        mod_name = module_.name
                        t = "#" * len(mod_name)
                        out += f"##{t}##\n# {mod_name} #\n##{t}##\n{module_.pp()}\n"
                    return out
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
                    return f"Invalid key: {error}"
        else:
            return "Not a .jac or .py file, or invalid command for file type."

    def autodoc_uninode(self) -> str:
        """Generate mermaid markdown doc for uninodes."""
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

    def automate_ref(self) -> str:
        """Automate the reference guide generation."""
        return auto_generate_refs()

    def gen_parser(self) -> str:
        """Generate static parser."""
        from jaclang.compiler import generate_static_parser

        generate_static_parser(force=True)
        return "Parser generated."
