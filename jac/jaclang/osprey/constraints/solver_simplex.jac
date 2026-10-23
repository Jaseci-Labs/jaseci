"""Constraint insertion and primal simplex algorithm."""

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
    _journal_begin,
    _journal_new_symbol_journaled,
    _journal_get_var_symbol,
    _journal_insert_row,
    _journal_touch_row,
    _journal_touch_objective,
    _journal_pop_row,
    _journal_rollback,
}

def _solver_add_core(s: any, c: Constraint, tag: Tag, jnl: MutationJournal) -> SolveResult {
    row = _solver_create_row(s, c, tag, jnl);
    subject = _solver_choose_subject(s, row, tag);

    # No valid entering subject: an all-dummy row is redundant when its
    # constant is zero (the dummy marker may enter the basis) and
    # unsatisfiable otherwise (kiwi addConstraint).
    if (
        _journal_kind_of(s, subject) == SymbolKind.INVALID
        and _solver_all_dummies(s, row)
    ) {
        if not near_zero(row.constant) {
            return SolveResult(
                ok=False,
                error=SolveError.UNSATISFIABLE,
                message="required system inconsistent",
            );
        }
        subject = tag.marker;
    }

    if _journal_kind_of(s, subject) == SymbolKind.INVALID {
        if not _solver_add_with_artificial_variable(s, row, jnl) {
            return SolveResult(
                ok=False,
                error=SolveError.UNSATISFIABLE,
                message="artificial variable could not reach zero",
            );
        }
    } else {
        row.solve_for(subject);
        _solver_substitute(s, subject, row, jnl);
        _journal_insert_row(s, subject, row, jnl);
    }

    # Optimize after every mutation. The target is lexicographic, so
    # higher tiers are exhausted before lower tiers are considered.
    return _solver_optimize_cost(s, jnl);
}

def _solver_rebuild_admitting(s: any, candidate: Constraint, factory: any) -> any {
    stored: list[StoredConstraint] = list(s.history);
    stored.append(StoredConstraint(
        expression=candidate.expression,
        relation=candidate.relation,
        strength=candidate.strength,
        content_key=constraint_key(candidate),
    ));

    orders: list[list[StoredConstraint]] = [
        stored,
        [_solver_terms_reversed(s, st) for st in stored],
        list(reversed(stored)),
        [_solver_terms_reversed(s, st) for st in reversed(stored)],
    ];

    for order in orders {
        attempt = _solver_replay_all(s, order, factory);
        if attempt is not None {
            return attempt;
        }
    }
    return None;
}

def _solver_terms_reversed(s: any, st: StoredConstraint) -> StoredConstraint {
    terms_rev = [];
    for t in st.expression.terms {
        terms_rev.append(Term(
            variable=Variable(id=t.variable.id),
            coefficient=t.coefficient,
        ));
    }
    return StoredConstraint(
        expression=Expression(terms=terms_rev, constant=st.expression.constant),
        relation=st.relation,
        strength=st.strength,
        provenance=st.provenance,
        content_key=st.content_key,
    );
}

def _solver_replay_all(s: any, order: list[StoredConstraint], factory: any) -> any {
    # Replay on a scratch tableau so `self` stays untouched unless the
    # caller adopts the result.
    scratch = factory();
    tags: dict[str, Tag] = {};
    for st in order {
        c = Constraint(
            expression=st.expression,
            relation=st.relation,
            strength=st.strength,
        );
        jnl = _journal_begin(scratch);
        tag = Tag();
        res = _solver_add_core(scratch, c, tag, jnl);
        if not res.ok {
            return None;
        }
        key = constraint_key(c);
        tags[key] = tag;
    }
    scratch.cns = tags;
    # Preserve the complete accepted set so a future rebuild after this
    # adoption does not silently forget constraints.
    scratch.history = list(order);
    return scratch;
}

def _solver_pivot(s: any, 
    entering: int,
    leaving: int,
    jnl: MutationJournal,
    extra: Row | None = None,
    reinsert: bool = True,
) -> None {
    row = _journal_pop_row(s, leaving, jnl);
    row.solve_for_symbols(leaving, entering);
    _solver_substitute(s, entering, row, jnl, extra);
    if reinsert {
        _journal_insert_row(s, entering, row, jnl);
    }
}

def _solver_adopt(s: any, bundle: any) -> None {
    s.rows = bundle.rows;
    s.kinds = bundle.kinds;
    s.var_symbols = bundle.var_symbols;
    s.objective = bundle.objective;
    s.id_tick = bundle.id_tick;
    s.cns = bundle.cns;
    # Stale worklist entries would reference old-symbol ids that now
    # denote different rows in the adopted tableau.
    s.infeasible_rows = bundle.infeasible_rows;
}

def _solver_create_row(s: any, c: Constraint, tag: Tag, jnl: MutationJournal) -> Row {
    row = Row(constant=c.expression.constant);
    # Substitute already-basic variables from the current tableau.
    for t in c.expression.terms {
        if not near_zero(t.coefficient) {
            symbol = _journal_get_var_symbol(s, t.variable, jnl);
            basic = s.rows.get(symbol);
            if basic is not None {
                row.insert_row(basic, t.coefficient);
            } else {
                row.insert_symbol(symbol, t.coefficient);
            }
        }
    }
    if c.relation == Relation.LEQ or c.relation == Relation.GEQ {
        coeff = 1.0 if c.relation == Relation.LEQ else -1.0;
        slack = _journal_new_symbol_journaled(s, SymbolKind.SLACK, jnl);
        tag.marker = slack;
        row.insert_symbol(slack, coeff);
        if c.strength == StrengthTier.REQUIRED {
            # A required inequality has only its non-negative slack.
            tag.other = 0;
        } else {
            # LEQ violation is positive expression, hence -error; GEQ
            # violation is negative expression, hence +error.
            error = _journal_new_symbol_journaled(s, SymbolKind.ERROR, jnl);
            tag.other = error;
            row.insert_symbol(error, -coeff);
            _solver_add_objective(s, error, strength_weight(c.strength), jnl);
        }
    } else {
        if c.strength == StrengthTier.REQUIRED {
            # Required equality: a dummy marker keeps the basis restricted.
            dummy = _journal_new_symbol_journaled(s, SymbolKind.DUMMY, jnl);
            tag.marker = dummy;
            row.insert_symbol(dummy);
        } else {
            # A soft equality needs two non-negative error
            # directions: v == eplus - eminus, i.e. v - eplus +
            # eminus = 0 (kiwi OP_EQ soft case). The marker keeps a
            # NEGATIVE coefficient so chooseSubject can pick it as
            # pivot subject when no external symbol is available.
            plus = _journal_new_symbol_journaled(s, SymbolKind.ERROR, jnl);
            minus = _journal_new_symbol_journaled(s, SymbolKind.ERROR, jnl);
            tag.marker = plus;
            tag.other = minus;
            row.insert_symbol(plus, -1.0);
            row.insert_symbol(minus, 1.0);
            weight = strength_weight(c.strength);
            _solver_add_objective(s, plus, weight, jnl);
            _solver_add_objective(s, minus, weight, jnl);
        }
    }
    if row.constant < 0.0 {
        row.reverse_sign();
    }
    return row;
}

def _solver_choose_subject(s: any, row: Row, tag: Tag) -> int {
    for symbol in sorted(row.cells.keys()) {
        if _journal_kind_of(s, symbol) == SymbolKind.EXTERNAL {
            return symbol;
        }
    }
    for candidate in [tag.marker, tag.other] {
        kind = _journal_kind_of(s, candidate);
        if (
            (kind == SymbolKind.SLACK or kind == SymbolKind.ERROR)
            and row.coefficient_for(candidate) < 0.0
        ) {
            return candidate;
        }
    }
    return 0;
}

def _solver_all_dummies(s: any, row: Row) -> bool {
    for symbol in sorted(row.cells.keys()) {
        if _journal_kind_of(s, symbol) != SymbolKind.DUMMY {
            return False;
        }
    }
    return True;
}

def _solver_any_pivotable_symbol(s: any, row: Row) -> int {
    for symbol in sorted(row.cells.keys()) {
        kind = _journal_kind_of(s, symbol);
        if kind == SymbolKind.SLACK or kind == SymbolKind.ERROR {
            return symbol;
        }
    }
    return 0;
}

def _solver_add_with_artificial_variable(s: any, row: Row, jnl: MutationJournal) -> bool {
    art = _journal_new_symbol_journaled(s, SymbolKind.SLACK, jnl);
    art_row = Row(constant=row.constant);
    art_row.cells = dict(row.cells);
    _journal_insert_row(s, art, art_row, jnl);

    # Artificial cost row; kept in sync by every pivot below
    # (kiwi m_artificial, substituted inside substitute()).
    artificial = Row(constant=row.constant);
    artificial.cells = dict(row.cells);
    _solver_optimize_toward(s, artificial, jnl, artificial);

    success = near_zero(artificial.constant);

    if art in (s.rows as dict[int, Row]) {
        pivot_row = _journal_pop_row(s, art, jnl);
        if len(pivot_row.cells) > 0 {
            entering = _solver_any_pivotable_symbol(s, pivot_row);
            if entering == 0 {
                return False;
            }
            pivot_row.insert_symbol(art, -1.0);
            pivot_row.solve_for(entering);
            _solver_substitute(s, entering, pivot_row, jnl, artificial);
            _journal_insert_row(s, entering, pivot_row, jnl);
        }
    }

    for symbol in sorted(s.rows.keys()) {
        _journal_touch_row(s, symbol, jnl);
        s.rows[symbol].remove_symbol(art);
    }
    _journal_touch_objective(s, jnl);
    s.objective.remove_symbol(art);
    return success;
}

def _solver_substitute(s: any,
    symbol: int,
    row: Row,
    jnl: MutationJournal,
    extra: Row | None = None,
) -> None {
    for row_symbol in sorted(s.rows.keys()) {
        _journal_touch_row(s, row_symbol, jnl);
        r = s.rows[row_symbol];
        r.substitute(symbol, row);
        # Negative non-external constants would be tracked for
        # dualOptimize from M3 onward (kiwi m_infeasible_rows).
    }
    _journal_touch_objective(s, jnl);
    s.objective.substitute(symbol, row);
    # The artificial cost row participates in its own pivots
    # (kiwi substitutes into m_artificial when present).
    if extra is not None {
        extra.substitute(symbol, row);
    }
    # Track rows driven out of feasibility so a later suggestion's
    # dualOptimize can repair them (kiwi m_infeasible_rows).
    for row_symbol in sorted(s.rows.keys()) {
        if (
            _journal_kind_of(s, row_symbol) != SymbolKind.EXTERNAL
            and s.rows[row_symbol].constant < 0.0
            and row_symbol not in (s.infeasible_rows as list[int])
        ) {
            s.infeasible_rows.append(row_symbol);
        }
    }
}

def _solver_add_objective(s: any, 
    symbol: int,
    weight: LexWeight,
    jnl: MutationJournal,
) -> None {
    if lex_is_zero(weight) {
        return;
    }
    _journal_touch_objective(s, jnl);
    s.objective.insert_symbol(symbol, weight);
    if symbol in (s.rows as dict[int, Row]) {
        s.objective.substitute(symbol, s.rows[symbol]);
    }
}

def _solver_optimize_cost(s: any, jnl: MutationJournal) -> SolveResult {
    while True {
        entering = _solver_get_entering_cost_symbol(s);
        if entering == 0 {
            return SolveResult(ok=True);
        }
        leaving = _solver_get_leaving_row(s, entering);
        if leaving == 0 {
            return SolveResult(
                ok=False,
                error=SolveError.INTERNAL_INVARIANT,
                message="lexicographic objective unbounded",
            );
        }
        _solver_pivot(s, entering, leaving, jnl);
    }
}

def _solver_optimize_toward(s: any, 
    target: Row,
    jnl: MutationJournal,
    extra: Row | None = None,
) -> SolveResult {
    while True {
        entering = _solver_get_entering_symbol(s, target);
        if entering == 0 {
            return SolveResult(ok=True);
        }
        leaving = _solver_get_leaving_row(s, entering);
        if leaving == 0 {
            return SolveResult(
                ok=False,
                error=SolveError.INTERNAL_INVARIANT,
                message="objective unbounded",
            );
        }
        _solver_pivot(s, entering, leaving, jnl, extra);
    }
}

def _solver_get_entering_symbol(s: any, objective: Row) -> int {
    for symbol in sorted(objective.cells.keys()) {
        if (
            _journal_kind_of(s, symbol) != SymbolKind.DUMMY
            and objective.cells[symbol] < 0.0
        ) {
            return symbol;
        }
    }
    return 0;
}

def _solver_get_entering_cost_symbol(s: any) -> int {
    for symbol in sorted(s.objective.cells.keys()) {
        if (
            _journal_kind_of(s, symbol) != SymbolKind.DUMMY
            and lex_is_negative(s.objective.cells[symbol])
        ) {
            return symbol;
        }
    }
    return 0;
}

def _solver_get_leaving_row(s: any, entering: int) -> int {
    ratio = 1e308;
    found = 0;
    for symbol in sorted(s.rows.keys()) {
        if _journal_kind_of(s, symbol) == SymbolKind.EXTERNAL {
            continue;
        }
        temp = s.rows[symbol].coefficient_for(entering);
        if temp < 0.0 {
            temp_ratio = -s.rows[symbol].constant / temp;
            if temp_ratio < ratio {
                ratio = temp_ratio;
                found = symbol;
            }
        }
    }
    return found;
}

