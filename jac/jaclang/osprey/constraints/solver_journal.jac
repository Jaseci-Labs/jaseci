"""Tableau bookkeeping and exact rollback journal operations."""

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

def _journal_expression_is_finite(s: any, e: Expression) -> bool {
    if not is_finite(e.constant) {
        return False;
    }
    for t in e.terms {
        if not is_finite(t.coefficient) {
            return False;
        }
    }
    return True;
}

def _journal_kind_of(s: any, symbol: int) -> SymbolKind {
    if symbol <= 0 {
        return SymbolKind.INVALID;
    }
    return s.kinds.get(symbol, SymbolKind.INVALID);
}

def _journal_begin(s: any) -> MutationJournal {
    return MutationJournal(
        id_tick_start=s.id_tick,
        infeasible_start=len(s.infeasible_rows),
    );
}

def _journal_witness_for_key(s: any, key: str) -> list[str] {
    out: list[str] = [];
    for hid in sorted(s.handle_keys.keys()) {
        if s.handle_keys[hid] == key and s.provenance.get(hid, "") != "" {
            out.append(s.provenance[hid]);
        }
    }
    return out;
}

def _journal_witness_extra(s: any, extra: str) -> list[str] {
    if extra == "" {
        return [];
    }
    return [extra];
}

def _journal_new_symbol(s: any, kind: SymbolKind) -> int {
    symbol = s.id_tick;
    s.id_tick += 1;
    s.kinds[symbol] = kind;
    return symbol;
}

def _journal_new_symbol_journaled(s: any, kind: SymbolKind, jnl: MutationJournal) -> int {
    symbol = _journal_new_symbol(s, kind);
    jnl.allocated_symbols.append(symbol);
    return symbol;
}

def _journal_get_var_symbol(s: any, v: Variable, jnl: MutationJournal | None = None) -> int {
    var_symbols: dict[int, int] = s.var_symbols;
    if v.id in var_symbols {
        return var_symbols[v.id];
    }
    symbol = _journal_new_symbol(s, SymbolKind.EXTERNAL);
    s.var_symbols[v.id] = symbol;
    if jnl is not None {
        jnl.new_var_ids.append(v.id);
        jnl.allocated_symbols.append(symbol);
    }
    return symbol;
}

def _journal_insert_row(s: any, symbol: int, row: Row, jnl: MutationJournal) -> None {
    if (
        symbol not in jnl.inserted_rows
        and symbol not in jnl.row_snapshots
    ) {
        jnl.inserted_rows.append(symbol);
    }
    s.rows[symbol] = row;
}

def _journal_touch_row(s: any, symbol: int, jnl: MutationJournal) -> None {
    rows: dict[int, Row] = s.rows;
    if (
        symbol in rows
        and symbol not in jnl.row_snapshots
        and symbol not in jnl.inserted_rows
    ) {
        jnl.row_snapshots[symbol] = rows[symbol].clone();
    }
}

def _journal_touch_objective(s: any, jnl: MutationJournal) -> None {
    if jnl.objective_snapshot is None {
        jnl.objective_snapshot = s.objective.clone();
    }
}

def _journal_pop_row(s: any, symbol: int, jnl: MutationJournal) -> Row {
    _journal_touch_row(s, symbol, jnl);
    return s.rows.pop(symbol);
}

def _journal_rollback(s: any, jnl: MutationJournal) -> None {
    rows: dict[int, Row] = s.rows;
    # 1. Drop rows created during the operation.
    for symbol in reversed(jnl.inserted_rows) {
        if symbol in rows {
            rows.pop(symbol);
        }
    }
    # 2. Restore pre-existing rows to pre-mutation state; re-inserts
    #    rows optimize() may have moved or removed.
    for symbol in sorted(jnl.row_snapshots.keys()) {
        rows[symbol] = jnl.row_snapshots[symbol].clone();
    }
    # 3. Restore the objective row.
    if jnl.objective_snapshot is not None {
        s.objective = jnl.objective_snapshot.clone();
    }
    # 4. Unregister external variables introduced here.
    for vid in reversed(jnl.new_var_ids) {
        s.var_symbols.pop(vid);
    }
    # 5. Release symbols and rewind the id counter.
    for symbol in reversed(jnl.allocated_symbols) {
        s.kinds.pop(symbol);
    }
    s.id_tick = jnl.id_tick_start;
    # 6. Drop worklist entries recorded during the failed operation.
    del s.infeasible_rows[jnl.infeasible_start:];
}

