"""Jac Blue pass for drawing AST."""
import inspect

import jaclang.jac.absyntree as ast
from jaclang.jac.absyntree import Ability, AbilityDef, ArchDef, Architype
from jaclang.jac.passes import Pass


DOT_GRAPH_CLASS_COLOR_MAP: dict[type, str] = {
    Architype: "red",
    Ability: "green",
    ArchDef: "blue",
    AbilityDef: "yellow",
}


class DotGraphPass(Pass):
    """Jac AST convertion to DOT graph."""

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__dot_lines: list[str] = []
        self.__id_map: dict[int, int] = {}
        self.__lase_id_used = 0
        return super().before_pass()

    def __gen_node_id(self, node: ast.AstNode) -> int:
        if id(node) not in self.__id_map:
            self.__id_map[id(node)] = self.__lase_id_used
            self.__lase_id_used += 1
        return self.__id_map[id(node)]

    def __gen_node_parameters(self, node: ast.AstNode) -> str:
        shape = ""
        fillcolor = ""
        style = ""
        if node.__class__ in DOT_GRAPH_CLASS_COLOR_MAP:
            shape = 'shape="box"'
            style = 'style="filled"'
            fillcolor = f'fillcolor="{DOT_GRAPH_CLASS_COLOR_MAP[node.__class__]}"'

        info = self.__gen_node_info(node)
        if len(info) == 0:
            label = f'"{node.__class__.__name__}"'
        else:
            label = f"<{node.__class__.__name__}"
            for i in info:
                label += f"<BR/> {i[0]}: {i[1]}"
            label += ">"

        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def __gen_node_info(self, node: ast.AstNode) -> list[tuple[str, str]]:
        init_source = inspect.getsource(node.__class__.__init__)
        info_to_be_dumped: list[tuple[str, str]] = []
        for line in init_source.split("\n"):
            if "def" in line:
                continue
            elif "->" in line:
                break
            elif "# DotExporter::AddInfo" in line:
                info_to_be_dumped.append(
                    (
                        line.strip().split(":")[0].strip(),
                        line.strip().split(":")[1].split("#")[0].strip(),
                    )
                )
        return info_to_be_dumped

    def enter_node(self, node: ast.AstNode) -> None:
        """Enter node."""
        self.__dot_lines.append(
            f"{self.__gen_node_id(node)} {self.__gen_node_parameters(node)};"
        )
        for kid_node in node.kid:
            if kid_node:
                self.__dot_lines.append(
                    f"{self.__gen_node_id(node)}  -> {self.__gen_node_id(kid_node)};"
                )

    def after_pass(self) -> None:
        """Finalize pass by generating the dot file."""
        with open("out.dot", "w") as f:
            f.write("digraph graph1 {")
            f.write("\n".join(self.__dot_lines))
            f.write("}")
        return super().after_pass()
