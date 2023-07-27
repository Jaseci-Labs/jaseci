"""Constants across the project."""
from enum import Enum, auto


class Constants(str, Enum):
    """Token constants for Jac."""

    INIT_FUNC = "init"
    JAC_LANG_IMP = "jac"
    JAC_DEBUG_SPLITTER = "JAC DEBUG INFO"
    PATCH = "PATCH"

    JAC_TMP = "_jac_tmp"
    EXEC_CONTEXT = "_jac_exec_ctx_"
    HERE = "_jac_here_"
    ROOT = f"{EXEC_CONTEXT}.get_root()"
    EDGES_TO_NODE = "_jac_edges_to_nodes_"
    EDGE_REF = "_jac_edge_ref_"
    CONNECT_NODE = "_jac_connect_node_"
    DISCONNECT_NODE = "_jac_disconnect_node_"
    WALKER_VISIT = "_jac_visit_"
    DISENGAGE = "_jac_disengage_"
    OBJECT_CLASS = "_jac_Object_"
    NODE_CLASS = "_jac_Node_"
    EDGE_CLASS = "_jac_Edge_"
    WALKER_CLASS = "_jac_Walker_"
    WITH_DIR = "_jac_apply_dir_"
    EDGE_DIR = "_jac_Edge_Dir_"

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
