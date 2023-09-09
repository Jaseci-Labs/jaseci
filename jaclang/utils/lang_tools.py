"""Language tools for the Jaclang project."""

import inspect
import sys
from typing import Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer
from jaclang.utils.helpers import pascal_to_snake


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

    def process(self, cls: type) -> None:
        """Process AstNode class."""
        self.class_name = cls.__name__
        AstNodeInfo.type_map[self.class_name] = cls
        self.class_name_snake = pascal_to_snake(cls.__name__)
        self.init_sig = inspect.signature(cls.__init__)
        self.kids: list[AstKidInfo] = []
        for param_name, param in self.init_sig.parameters.items():
            if param_name not in ["self", "parent", "kid", "line"]:
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
            AstNodeInfo(cls) for _, cls in classes if issubclass(cls, ast.AstNode)
        ]
        self.ast_classes = sorted(
            ast_node_classes,
            key=lambda cls: source_code.find(f"class {cls.class_name}"),
        )

    def pass_template(self) -> str:
        """Generate pass template."""
        output = "import jaclang.jac.absyntree as ast\nfrom jaclang.jac.passes import Pass\n\nclass SomePass(Pass):\n"

        def emit(to_append: str) -> None:
            """Emit to output."""
            nonlocal output
            output += "\n    " + to_append

        for cls in self.ast_classes:
            emit(
                f"def exit_{cls.class_name_snake}(self, node: ast.{cls.class_name}) -> None:\n"
            )
            emit('    """Sub objects.\n')

            for kid in cls.kids:
                emit(
                    f"    {kid.name}: {kid.typ}{' ='+kid.default if kid.default else ''},"
                )

            emit('    """\n')
        output = (
            output.replace("jaclang.jac.absyntree.", "")
            .replace("typing.", "")
            .replace("<enum '", "")
            .replace("'>", "")
            .replace("<class '", "")
            .replace("ForwardRef('", "")
            .replace("')", "")
        )
        return output

    def jac_keywords(self) -> str:
        """Get all Jac keywords as an or string."""
        ret = ""
        for k in JacLexer._remapping["NAME"].keys():
            ret += f"{k}|"
        return ret[:-1]

    def md_doc(self) -> str:
        """Generate mermaid markdown doc."""
        output = ""
        for cls in self.ast_classes:
            output += "```mermaid\nclassDiagram\n"
            for kid in cls.kids:
                output += f"{cls.class_name} --> {kid.name}: {kid.typ} \n"
            output += "```\n"
        return output
