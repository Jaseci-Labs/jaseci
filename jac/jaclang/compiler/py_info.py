"""Code location info for AST nodes."""

from __future__ import annotations


class PyInfo:
    """Python info related to python imports."""

    def __init__(self) -> None:
        # Module dependacy map used to store all module dependacies detected
        # by mypy. The dependacies are computed using the mypy graph in
        # TypeCheck pass
        self.py_mod_dep_map: dict[str, str] = {}

        # Flag for python modules raised into jac
        self.is_raised_from_py: bool = False
