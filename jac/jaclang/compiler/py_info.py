"""Code location info for AST nodes."""

from __future__ import annotations


class PyInfo:
    """Python info related to python imports."""

    def __init__(self) -> None:
        """Object Initialization."""
        # Module dependacy map used to store all module dependacies detected
        # by mypy. The dependacies are computed using the mypy graph in
        # TypeCheck pass
        self.py_mod_dep_map: dict[str, str] = {}

        # Get all the modules that we really need to raise inorder to make
        # all Jac types correct (FuseTypeInfo works). This is computed using
        # PyCollectDepsPass.
        self.py_raise_map: dict[str, str] = {}

        # Flag for python modules raised into jac
        self.is_raised_from_py: bool = False
