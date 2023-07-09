"""Collection of purple passes for Jac IR."""
from jaclang import jac_import
from jaclang.jac.passes.blue import pass_schedule


purple = jac_import("purple_pygen_pass")
PurplePygenPass = purple.PurplePygenPass  # type: ignore

__all__ = [
    "PurplePygenPass",
]


pass_schedule = [
    *pass_schedule,
    PurplePygenPass,
]
