"""Constants across the project."""
from enum import Enum

class Constants(str, Enum):
    """Token constants for Jac."""

    INIT_FUNC = "init"
    JAC_LANG_IMP = "jac"

    EXEC_CONTEXT = "__jac_exec_ctx__"
    HERE = "__jac_here__"
    CONNECT_NODE = "__jac_connect_node__"
    OBJECT_CLASS = "__jac_Object__"
    NODE_CLASS = "__jac_Node__"
    EDGE_CLASS = "__jac_Edge__"
    WALKER_CLASS = "__jac_Walker__"
    WITH_DIR = "__jac_edge_with_dir__"

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return self.value

