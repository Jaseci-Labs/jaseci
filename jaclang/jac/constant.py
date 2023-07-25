"""Constants across the project."""
from enum import Enum, auto


class Constants(str, Enum):
    """Token constants for Jac."""

    INIT_FUNC = "init"
    JAC_LANG_IMP = "jac"
    JAC_DEBUG_SPLITTER = "JAC DEBUG INFO"
    PATCH = "PATCH"

    JAC_TMP = "_jac_tmp"
    EXEC_CONTEXT = "_jac_exec_ctx__"
    HERE = "_jac_here__"
    ROOT = f"{EXEC_CONTEXT}.get_root()"
    NODE_EDGES = "_jac_edges__"
    EDGE_REF = "_jac_edge_ref__"
    CONNECT_NODE = "_jac_connect_node__"
    DISCONNECT_NODE = "_jac_disconnect_node__"
    WALKER_VISIT = "_jac_visit__"
    OBJECT_CLASS = "_jac_Object__"
    NODE_CLASS = "_jac_Node__"
    EDGE_CLASS = "_jac_Edge__"
    WALKER_CLASS = "_jac_Walker__"
    WITH_DIR = "_jac_edge_with_dir__"
    EDGE_DIR = "_jac_Edge_Dir__"

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
