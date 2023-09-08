"""Language tools for the Jaclang project."""

import inspect
import sys

import jaclang.jac.absyntree as ast
from jaclang.utils.helpers import pascal_to_snake


class AstTool:
    """Ast tools."""

    def __init__(self) -> None:
        """Initialize."""
        self.ast_classes = self.get_ast_classes()

    def get_ast_classes(self) -> list[type]:
        """Analyze ast module."""
        module = sys.modules[ast.__name__]
        source_code = inspect.getsource(module)
        classes = inspect.getmembers(module, inspect.isclass)
        ast_node_classes = [cls for _, cls in classes if issubclass(cls, ast.AstNode)]
        return sorted(
            ast_node_classes, key=lambda cls: source_code.find(f"class {cls.__name__}")
        )

    def pass_template(self) -> str:
        """Generate pass template."""
        output = "import jaclang.jac.absyntree as ast\nfrom jaclang.jac.passes import Pass\n\nclass SomePass(Pass):\n"

        def emit(to_append: str) -> None:
            """Emit to output."""
            nonlocal output
            output += "\n    " + to_append

        for cls in self.ast_classes:
            class_name = cls.__name__
            snake_case_name = pascal_to_snake(class_name)

            emit(f"def exit_{snake_case_name}(self, node: ast.{class_name}) -> None:\n")
            emit('    """Sub objects.\n')

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
                        param.default
                        if param.default != inspect.Parameter.empty
                        else None
                    )
                    emit(
                        f"    {param_name}: {param_type}{' ='+param_default if param_default else ''},"
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

    def mermaid_md_doc(self) -> str:
        """Generate mermaid markdown doc."""
        return "need to implement"
