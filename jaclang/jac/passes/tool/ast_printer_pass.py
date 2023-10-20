"""Jac Blue pass for drawing AST."""
import inspect
from typing import List, Optional

import jaclang.jac.absyntree as ast
from jaclang.jac.absyntree import Ability, AbilityDef, ArchDef, Architype
from jaclang.jac.passes import Pass


DOT_GRAPH_CLASS_COLOR_MAP: dict[type, str] = {
    Architype: "red",
    Ability: "green",
    ArchDef: "blue",
    AbilityDef: "yellow",
}


class AstDotGraphPass(Pass):
    """Jac AST convertion to DOT graph."""

    OUTPUT_FILE_PATH: Optional[str] = "out.dot"

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
        if isinstance(node, ast.Token):
            shape = 'shape="box"'

        info = self.__gen_node_info(node)
        if len(info) == 0:
            label = f'"{node.__class__.__name__}"'
        else:
            label = f"<{node.__class__.__name__}"
            for i in info:
                label += f"<BR/> {i[0]}{i[1]}{i[2]}"
            label += ">"

        label = f"{label} {shape} {style} {fillcolor}".strip()
        return f"[label={label}]"

    def __gen_node_info(self, node: ast.AstNode) -> list[tuple[str, str, str]]:
        info_of_type = ":"
        info_of_value = "="
        # Get info from the fieds and their types from the constructors
        init_source = inspect.getsource(node.__class__.__init__)
        info_to_be_dumped: list[tuple[str, str, str]] = []
        for line in init_source.split("\n"):
            if "def" in line:
                continue
            elif "->" in line:
                break
            elif "# DotExporter::AddInfo" in line:
                info_to_be_dumped.append(
                    (
                        line.strip().split(":")[0].strip(),
                        info_of_type,
                        line.strip().split(":")[1].split("#")[0].strip(),
                    )
                )
        # Get token value and name
        if isinstance(node, ast.Token):
            info_to_be_dumped.append(("name", info_of_value, node.name))
            info_to_be_dumped.append(("value", info_of_value, node.value))
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
        if self.OUTPUT_FILE_PATH:
            with open(self.OUTPUT_FILE_PATH, "w") as f:
                f.write("digraph graph1 {")
                f.write("\n".join(self.__dot_lines))
                f.write("}")
        else:
            print("digraph graph1 {")
            print("\n".join(self.__dot_lines))
            print("}")
        return super().after_pass()


class AstPrinterPass(Pass):
    """Jac AST convertion to ascii tree."""

    SAVE_OUTPUT: Optional[str] = None

    def before_pass(self) -> None:
        """Initialize pass."""
        self.__print_tree(self.ir)
        self.terminate()
        return super().before_pass()

    def __print_tree(
        self,
        root: ast.AstNode,
        marker: str = "+-- ",
        level_markers: Optional[List[bool]] = None,
    ) -> None:
        """Recursive function that prints the hierarchical structure of a tree."""
        if root is None:
            return

        empty_str = " " * len(marker)
        connection_str = "|" + empty_str[:-1]
        if not level_markers:
            level_markers = []
        level = len(level_markers)  # recursion level

        def mapper(draw: bool) -> str:
            return connection_str if draw else empty_str

        markers = "".join(map(mapper, level_markers[:-1]))
        markers += marker if level > 0 else ""
        if self.SAVE_OUTPUT:
            with open(self.SAVE_OUTPUT, "a+") as f:
                print(f"{markers}{self.__node_repr_in_tree(root)}", file=f)
        else:
            print(f"{markers}{self.__node_repr_in_tree(root)}")
        # After root has been printed, recurse down (depth-first) the child nodes.
        for i, child in enumerate(root.kid):
            # The last child will not need connection markers on the current level
            # (see example above)
            is_last = i == len(root.kid) - 1
            self.__print_tree(child, marker, [*level_markers, not is_last])

    def __node_repr_in_tree(self, node: ast.AstNode) -> str:
        if isinstance(node, ast.Token):
            return f"{node.__class__.__name__} - {node.value}"
            # return f"{node.__class__.__name__}({node.name}, {node.value})"
        else:
            return node.__class__.__name__
