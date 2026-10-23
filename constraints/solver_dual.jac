"""Constraint removal and dual simplex algorithm."""

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
    _journal_kind_of,
    _journal_touch_row,
    _journal_touch_objective,
    _journal_pop_row,
}
import from .solver_simplex {
    _solver_pivot,
    _solver_optimize_cost,
}

def _solver_remove_core(s: any, tag: Tag, strength: StrengthTier, jnl: MutationJournal) -> SolveResult {
    # Remove the error effects from the objective BEFORE pivoting, or
    # substitutions into the objective would double-count them.
    _solver_remove_constraint_effects(s, tag, strength, jnl);
    marker = tag.marker;
    if marker in (s.rows as dict[int, Row]) {
        # Marker is basic: simply drop the row.
        _journal_pop_row(s, marker, jnl);
    } else {
        leaving = _solver_get_marker_leaving_row(s, marker);
        if leaving == 0 {
            return SolveResult(
                ok=False,
                error=SolveError.INTERNAL_INVARIANT,
                message="failed to find leaving row",
            );
        }
        _solver_pivot(s, marker, leaving, jnl, reinsert=False);
    }
    # Optimize so the solver stays consistent after removal.
    return _solver_optimize_cost(s, jnl);
}

def _solver_remove_constraint_effects(s: any, 
    tag: Tag,
    strength: StrengthTier,
    jnl: MutationJournal,
) -> None {
    weight = strength_weight(strength);
    if lex_is_zero(weight) {
        return;
    }
    if _journal_kind_of(s, tag.marker) == SymbolKind.ERROR {
        _solver_remove_marker_effects(s, tag.marker, weight, jnl);
    }
    if _journal_kind_of(s, tag.other) == SymbolKind.ERROR {
        _solver_remove_marker_effects(s, tag.other, weight, jnl);
    }
}

def _solver_remove_marker_effects(s: any, 
    marker: int,
    weight: LexWeight,
    jnl: MutationJournal,
) -> None {
    _journal_touch_objective(s, jnl);
    row = s.rows.get(marker);
    if row is not None {
        s.objective.insert_row(row, lex_neg(weight));
    } else {
        s.objective.insert_symbol(marker, lex_neg(weight));
    }
}

def _solver_get_marker_leaving_row(s: any, marker: int) -> int {
    ratio1 = 1e308;
    ratio2 = 1e308;
    first = 0;
    second = 0;
    third = 0;
    for symbol in sorted(s.rows.keys()) {
        coeff = s.rows[symbol].coefficient_for(marker);
        if near_zero(coeff) {
            continue;
        }
        if _journal_kind_of(s, symbol) == SymbolKind.EXTERNAL {
            third = symbol;
        } elif coeff < 0.0 {
            r = -s.rows[symbol].constant / coeff;
            if r < ratio1 {
                ratio1 = r;
                first = symbol;
            }
        } else {
            r = s.rows[symbol].constant / coeff;
            if r < ratio2 {
                ratio2 = r;
                second = symbol;
            }
        }
    }
    if first != 0 {
        return first;
    }
    if second != 0 {
        return second;
    }
    return third;
}

def _solver_dual_optimize(s: any, jnl: MutationJournal) -> SolveResult {
    while len(s.infeasible_rows) > 0 {
        leaving = s.infeasible_rows.pop();
        row = s.rows.get(leaving);
        if (
            row is None
            or near_zero(row.constant)
            or row.constant >= 0.0
        ) {
            continue;
        }
        entering = _solver_get_dual_entering_symbol(s, row);
        if entering == 0 {
            return SolveResult(
                ok=False,
                error=SolveError.INTERNAL_INVARIANT,
                message="dual optimize failed",
            );
        }
        _solver_pivot(s, entering, leaving, jnl);
    }
    return SolveResult(ok=True);
}

def _solver_get_dual_entering_symbol(s: any, row: Row) -> int {
    entering = 0;
    best_coeff = 0.0;
    for symbol in sorted(row.cells.keys()) {
        cell = row.cells[symbol];
        if cell <= 0.0 or _journal_kind_of(s, symbol) == SymbolKind.DUMMY {
            continue;
        }
        if entering == 0 or _solver_dual_ratio_less(s, 
            _solver_objective_weight(s, symbol),
            cell,
            _solver_objective_weight(s, entering),
            best_coeff,
        ) {
            entering = symbol;
            best_coeff = cell;
        }
    }
    return entering;
}

def _solver_objective_weight(s: any, symbol: int) -> LexWeight {
    return s.objective.cells.get(symbol, lex_zero());
}

def _solver_dual_ratio_less(s: any, 
    w1: LexWeight,
    c1: float,
    w2: LexWeight,
    c2: float,
) -> bool {
    return lex_compare(lex_scale(w1, c2), lex_scale(w2, c1)) < 0;
}

def _solver_apply_suggestion(s: any, 
    info: EditInfo,
    delta: float,
    jnl: MutationJournal,
) -> None {
    marker = s.cns[info.key].marker;
    other = s.cns[info.key].other;
    row = s.rows.get(marker);
    if row is not None {
        _journal_touch_row(s, marker, jnl);
        if row.add(-delta) < 0.0 {
            s.infeasible_rows.append(marker);
        }
        return;
    }
    row = s.rows.get(other);
    if row is not None {
        _journal_touch_row(s, other, jnl);
        if row.add(delta) < 0.0 {
            s.infeasible_rows.append(other);
        }
        return;
    }
    for symbol in sorted(s.rows.keys()) {
        r = s.rows[symbol];
        coeff = r.coefficient_for(marker);
        if near_zero(coeff) {
            continue;
        }
        _journal_touch_row(s, symbol, jnl);
        if r.add(delta * coeff) < 0.0 {
            if _journal_kind_of(s, symbol) != SymbolKind.EXTERNAL {
                s.infeasible_rows.append(symbol);
            }
        }
    }
}

