"""Constants across the project."""
from enum import Enum, auto


class Constants(str, Enum):
    """Token constants for Jac."""

    INIT_FUNC = "init"
    JAC_LANG_IMP = "jac"
    JAC_DEBUG_SPLITTER = "JAC DEBUG INFO"
    PATCH = "PATCH"

    JAC_TMP = "__jac_tmp"
    EXEC_CONTEXT = "__jac_exec_ctx__"
    HERE = "__jac_here__"
    ROOT = f"{EXEC_CONTEXT}.get_root()"
    NODE_EDGES = "__jac_edges__"
    EDGE_REF = "__jac_edge_ref__"
    CONNECT_NODE = "__jac_connect_node__"
    DISCONNECT_NODE = "__jac_disconnect_node__"
    WALKER_VISIT = "__jac_visit__"
    OBJECT_CLASS = "__jac_Object__"
    NODE_CLASS = "__jac_Node__"
    EDGE_CLASS = "__jac_Edge__"
    WALKER_CLASS = "__jac_Walker__"
    WITH_DIR = "__jac_edge_with_dir__"
    EDGE_DIR = "__jac_Edge_Dir__"

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return self.value


class EdgeDir(Enum):
    """Edge direction indicator."""

    IN = auto()
    OUT = auto()
    ANY = auto()


class Values(int, Enum):
    """Token constants for Jac."""

    JAC_ERROR_LINE_RANGE = 3

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return self.value
