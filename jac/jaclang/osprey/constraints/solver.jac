"""Constraint solver compatibility facade.

The public Solver and its historical imported symbols remain here; tableau
rows, journaling, primal simplex, and dual simplex live in focused modules.
"""

import from .algebra {
    EPSILON,
    Constraint,
    Expression,
    LexWeight,
    Relation,
    StrengthTier,
    Term,
    Variable,
    constraint_key,
    is_finite,
    lex_add,
    lex_compare,
    lex_is_negative,
    lex_is_zero,
    lex_neg,
    lex_scale,
    lex_zero,
    near_zero,
    normalize_expression,
    strength_weight,
    term,
}
import from .results {
    ConstraintHandle,
    SolveError,
    SolveResult,
    SolverSnapshot,
}
import from .solver_types {
    SymbolKind,
    MutationJournal,
    Tag,
    Row,
    CostRow,
    StoredConstraint,
    EditInfo,
}

import from .solver_journal {
    _journal_expression_is_finite,
    _journal_begin,
    _journal_rollback,
    _journal_witness_for_key,
    _journal_witness_extra,
}
import from .solver_simplex {
    _solver_add_core,
    _solver_rebuild_admitting,
    _solver_replay_all,
    _solver_adopt,
}
import from .solver_dual {
    _solver_remove_core,
    _solver_dual_optimize,
    _solver_apply_suggestion,
}

def _new_solver() -> Solver { return Solver(); }

obj Solver {
    has rows: dict[int, Row] = {},
        kinds: dict[int, SymbolKind] = {},
        var_symbols: dict[int, int] = {},
        # Content key -> tag (kiwi m_cns, keyed by constraint identity).
        cns: dict[str, Tag] = {},
        # Handle id -> content key; provenance by handle id.
        handle_keys: dict[int, str] = {},
        provenance: dict[int, str] = {},
        next_handle_id: int = 1,
        objective: CostRow = CostRow(),
        id_tick: int = 1,
        # Variable ids never collide across table rebuilds.
        next_var_id: int = 1,
        # Accepted constraints in insertion order (rebuild input).
        history: list[StoredConstraint] = [],
        # var id -> edit bookkeeping (kiwi m_edits).
        edits: dict[int, EditInfo] = {},
        # LIFO worklist of possibly-infeasible row symbols (kiwi
        # m_infeasible_rows); drained by dualOptimize after suggestions.
        infeasible_rows: list[int] = [],
        # Monotonic; increments only on successful mutation (plan §5.4).
        generation: int = 0;

    """Allocate a fresh external variable with a unique id.

    Variable ids and symbol ids share the id_tick sequence but never mix:
    each allocated variable later receives its own distinct external
    symbol via _get_var_symbol (kiwi keeps them in separate namespaces)."""
    def new_variable() -> Variable {
        v = Variable(id=self.next_var_id);
        self.next_var_id += 1;
        return v;
    }

    def add_constraint(c_raw: Constraint, provenance: str = "") -> SolveResult {
        # Finite-value rejection happens on the RAW expression before
        # normalization, which itself asserts finiteness (plan §5.3: typed
        # outcomes, not exceptions, at the interface).
        if not _journal_expression_is_finite(self, c_raw.expression) {
            return SolveResult(ok=False, error=SolveError.NON_FINITE_VALUE);
        }
        c = Constraint(
            expression=normalize_expression(c_raw.expression),
            relation=c_raw.relation,
            strength=c_raw.strength,
        );
        key = constraint_key(c);
        if key in self.cns {
            return SolveResult(
                ok=False,
                error=SolveError.DUPLICATE_CONSTRAINT,
                witness_provenance=_journal_witness_for_key(self, key),
            );
        }

        # Fast path: incremental add on the live tableau.
        jnl = _journal_begin(self);
        tag = Tag();
        res = _solver_add_core(self, c, tag, jnl);
        if not res.ok {
            _journal_rollback(self, jnl);
            if res.error != SolveError.UNSATISFIABLE {
                res.witness_provenance = _journal_witness_extra(self, provenance);
                return res;
            }
            # DELIBERATE DIVERGENCE FROM KIWI (plan §8.2, decision D20):
            # the upstream kernel's artificial-variable phase is pivot-
            # order sensitive and can spuriously reject feasible required
            # systems depending on symbol allocation order (verified
            # against nucleic/kiwi C++ master). On UNSATISFIABLE we
            # rebuild the whole system from stored history under a small
            # set of fixed deterministic elimination orders and accept if
            # any rebuild admits the new constraint. Failure across all
            # orders is reported as UNSATISFIABLE.
            rebuilt = _solver_rebuild_admitting(self, c, _new_solver);
            if rebuilt is None {
                return SolveResult(
                    ok=False,
                    error=SolveError.UNSATISFIABLE,
                    message="required system inconsistent under all "
                            + "elimination orders",
                    witness_provenance=_journal_witness_extra(self, provenance),
                );
            }
            _solver_adopt(self, rebuilt);
        }

        # Commit: register handle + provenance, bump generation. On the
        # fast path the tag comes from the live add; after a rebuild the
        # rebuilt tags are already installed under the same content keys.
        handle = ConstraintHandle(id=self.next_handle_id);
        self.next_handle_id += 1;
        if key not in self.cns {
            self.cns[key] = tag;
        }
        self.handle_keys[handle.id] = key;
        self.provenance[handle.id] = provenance;
        self.history.append(StoredConstraint(
            expression=c.expression,
            relation=c.relation,
            strength=c.strength,
            provenance=provenance,
            content_key=key,
        ));
        self.generation += 1;
        return SolveResult(ok=True, handle=handle);

    }

    def has_constraint(handle: ConstraintHandle) -> bool {
        return handle.id in self.handle_keys;
    }

    def provenance_of(handle: ConstraintHandle) -> str {
        return self.provenance.get(handle.id, "");
    }

    # Compatibility hooks retained for the solver test annex and existing
    # diagnostic callers; algorithm bodies live in solver_simplex.
    def _replay_all(order: list[StoredConstraint]) -> Solver | None {
        return _solver_replay_all(self, order, _new_solver) as Solver;
    }

    def _adopt(bundle: Solver) -> None {
        _solver_adopt(self, bundle);
    }

    def remove_constraint(handle: ConstraintHandle) -> SolveResult {
        if handle.id not in self.handle_keys {
            return SolveResult(ok=False, error=SolveError.UNKNOWN_CONSTRAINT);
        }
        key = self.handle_keys[handle.id];
        if key not in self.cns {
            return SolveResult(ok=False, error=SolveError.UNKNOWN_CONSTRAINT);
        }
        tag = Tag(marker=self.cns[key].marker, other=self.cns[key].other);
        strength = solver_strength_for_key(self, key);
        jnl = _journal_begin(self);
        res = _solver_remove_core(self, tag, strength, jnl);
        if not res.ok {
            _journal_rollback(self, jnl);
            return res;
        }
        self.cns.pop(key);
        self.handle_keys.pop(handle.id);
        self.provenance.pop(handle.id);
        self.history = [
            st for st in self.history if st.content_key != key
        ];
        # An edit variable's underlying constraint was removed underneath
        # it; drop the registration so it cannot suggest again.
        for vid in sorted(self.edits.keys()) {
            if self.edits[vid].key == key {
                self.edits.pop(vid);
            }
        }
        self.generation += 1;
        return res;
    }

    def add_edit_variable(v: Variable, strength: StrengthTier) -> SolveResult {
        if v.id in self.edits {
            return SolveResult(
                ok=False,
                error=SolveError.DUPLICATE_EDIT_VARIABLE,
            );
        }
        if strength == StrengthTier.REQUIRED {
            return SolveResult(
                ok=False,
                error=SolveError.REQUIRED_EDIT_VARIABLE,
                message="edit variables cannot be required",
            );
        }
        # The edit variable is exactly a soft equality v == 0 (kiwi
        # addEditVariable); suggestions move its constant incrementally.
        c = Constraint(
            expression=normalize_expression(term(v)),
            relation=Relation.EQ,
            strength=strength,
        );
        res = self.add_constraint(c);
        if not res.ok {
            return res;
        }
        handle = res.handle;
        if handle is None {
            return SolveResult(
                ok=False,
                error=SolveError.INTERNAL_INVARIANT,
                message="accepted add returned no handle",
            );
        }
        self.edits[v.id] = EditInfo(
            var_id=v.id,
            key=self.handle_keys[handle.id],
            handle=handle,
        );
        return res;
    }

    def remove_edit_variable(v: Variable) -> SolveResult {
        if v.id not in self.edits {
            return SolveResult(ok=False, error=SolveError.UNKNOWN_EDIT_VARIABLE);
        }
        info = self.edits[v.id];
        res = self.remove_constraint(info.handle);
        # remove_constraint already dropped the edits entry for the
        # underlying constraint; nothing further to clean up.
        return res;
    }

    def has_edit_variable(v: Variable) -> bool {
        return v.id in self.edits;
    }

    def suggest_value(v: Variable, value: float) -> SolveResult {
        if not is_finite(value) {
            return SolveResult(ok=False, error=SolveError.NON_FINITE_VALUE);
        }
        if v.id not in self.edits {
            return SolveResult(ok=False, error=SolveError.UNKNOWN_EDIT_VARIABLE);
        }
        info = self.edits[v.id];
        if info.key not in self.cns {
            return SolveResult(ok=False, error=SolveError.UNKNOWN_EDIT_VARIABLE);
        }
        delta = value - info.constant;
        jnl = _journal_begin(self);
        _solver_apply_suggestion(self, info, delta, jnl);
        res = _solver_dual_optimize(self, jnl);
        if not res.ok {
            _journal_rollback(self, jnl);
            return res;
        }
        info.constant = value;
        self.generation += 1;
        return SolveResult(ok=True);
    }

    def snapshot() -> SolverSnapshot {
        vals: dict[int, float] = {};
        for vid in sorted(self.var_symbols.keys()) {
            symbol = self.var_symbols[vid];
            if symbol in self.rows {
                vals[vid] = self.rows[symbol].constant;
            } else {
                vals[vid] = 0.0;
            }
        }
        return SolverSnapshot(generation=self.generation, values=vals);
    }

    def reset() -> None {
        self.rows = {};
        self.kinds = {};
        self.var_symbols = {};
        self.cns = {};
        self.handle_keys = {};
        self.provenance = {};
        self.next_handle_id = 1;
        self.objective = CostRow();
        self.id_tick = 1;
        self.next_var_id = 1;
        self.history = [];
        self.edits = {};
        self.infeasible_rows = [];
        self.generation = 0;
    }

}

def solver_strength_for_key(s: Solver, key: str) -> StrengthTier {
    for st in s.history {
        if st.content_key == key {
            return st.strength;
        }
    }
    return StrengthTier.REQUIRED;
}

