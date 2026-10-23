"""Typed solver outcomes: handles, errors, results (LAYOUT-ENGINE-PLAN §3).

Handles are allocated by exactly one Solver; callers never choose ids.
A failed result carries ok=False, a non-OK error, no handle, and leaves
solver generation/state unchanged (plan §5.4).
"""

enum SolveError {
    OK = "ok",
    UNSATISFIABLE = "unsatisfiable",
    DUPLICATE_CONSTRAINT = "duplicate_constraint",
    UNKNOWN_CONSTRAINT = "unknown_constraint",
    FOREIGN_HANDLE = "foreign_handle",
    DUPLICATE_EDIT_VARIABLE = "duplicate_edit_variable",
    UNKNOWN_EDIT_VARIABLE = "unknown_edit_variable",
    REQUIRED_EDIT_VARIABLE = "required_edit_variable",
    NON_FINITE_VALUE = "non_finite_value",
    INVALID_EXPRESSION = "invalid_expression",
    INTERNAL_INVARIANT = "internal_invariant"
}


"""Opaque reference to one accepted constraint in one Solver."""
obj ConstraintHandle {
    has id: int;
}


"""Immutable-by-convention view of solver state (plan §5.4).

Generation is state-local monotonic: incremented on each successful
solver mutation, unchanged on failure. values() is a fresh deep copy;
solver rows/tags/objective are never exposed."""
obj SolverSnapshot {
    has generation: int,
        # variable id -> value
        values: dict[int, float] = {};
}


obj SolveResult {
    has ok: bool = True,
        error: SolveError = SolveError.OK,
        message: str = "",
        # Set only by a successful add_constraint.
        handle: ConstraintHandle | None = None,
        # Provenance strings of constraints implicated in a failure,
        # when known (plan §5.4: diagnostics with provenance).
        witness_provenance: list[str] = [];
}
