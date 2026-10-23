"""Shared solver rows, symbols, and mutation records."""

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

enum SymbolKind {
    INVALID = "invalid",
    EXTERNAL = "external",
    SLACK = "slack",
    ERROR = "error",
    DUMMY = "dummy"
}


obj Tag {
    has marker: int = 0,
        other: int = 0;
}


obj Row {
    has constant: float = 0.0,
        cells: dict[int, float] = {};

    def insert_symbol(symbol: int, coefficient: float = 1.0) -> None {
        self.cells[symbol] = self.cells.get(symbol, 0.0) + coefficient;
        if near_zero(self.cells[symbol]) {
            self.cells.pop(symbol);
        }
    }

    def insert_row(other: Row, coefficient: float = 1.0) -> None {
        self.constant += other.constant * coefficient;
        for symbol in sorted(other.cells.keys()) {
            coeff = other.cells[symbol] * coefficient;
            if not near_zero(coeff) {
                self.insert_symbol(symbol, coeff);
            }
        }
    }

    def remove_symbol(symbol: int) -> None {
        if symbol in self.cells {
            self.cells.pop(symbol);
        }
    }

    def reverse_sign() -> None {
        self.constant = -self.constant;
        for symbol in sorted(self.cells.keys()) {
            self.cells[symbol] = -self.cells[symbol];
        }
    }

    """a * x + rest = 0  =>  x = (-1/a) * rest - constant/a.
    The target symbol must exist in cells (kiwi solveFor)."""
    def solve_for(symbol: int) -> None {
        coeff = -1.0 / self.cells[symbol];
        self.cells.pop(symbol);
        self.constant *= coeff;
        for s in sorted(self.cells.keys()) {
            self.cells[s] *= coeff;
        }
    }

    """Solve so `lhs` enters and `rhs` leaves (kiwi solveFor lhs, rhs)."""
    def solve_for_symbols(lhs: int, rhs: int) -> None {
        self.insert_symbol(lhs, -1.0);
        self.solve_for(rhs);
    }

    def coefficient_for(symbol: int) -> float {
        return self.cells.get(symbol, 0.0);
    }

    # Shift the row constant; returns the new constant so callers can
    # detect infeasibility (kiwi Row::add).
    def add(delta: float) -> float {
        self.constant += delta;
        return self.constant;
    }

    # Deep copy used by the rollback journal.
    def clone() -> Row {
        r = Row(constant=self.constant);
        r.cells = dict(self.cells);
        return r;
    }

    def substitute(symbol: int, row: Row) -> None {
        if symbol not in self.cells {
            return;
        }
        coefficient = self.cells.pop(symbol);
        self.insert_row(row, coefficient);
    }
}


obj CostRow {
    has constant: LexWeight = LexWeight(),
        cells: dict[int, LexWeight] = {};

    def insert_symbol(symbol: int, coefficient: LexWeight) -> None {
        if lex_is_zero(coefficient) {
            return;
        }
        current = self.cells.get(symbol, lex_zero());
        updated = lex_add(current, coefficient);
        if lex_is_zero(updated) {
            self.cells.pop(symbol);
        } else {
            self.cells[symbol] = updated;
        }
    }

    def insert_row(other: Row, coefficient: LexWeight) -> None {
        self.constant = lex_add(
            self.constant,
            lex_scale(coefficient, other.constant),
        );
        for symbol in sorted(other.cells.keys()) {
            self.insert_symbol(
                symbol,
                lex_scale(coefficient, other.cells[symbol]),
            );
        }
    }

    def remove_symbol(symbol: int) -> None {
        if symbol in self.cells {
            self.cells.pop(symbol);
        }
    }

    def clone() -> CostRow {
        copy = CostRow(constant=LexWeight(tiers=[
            self.constant.tiers[0],
            self.constant.tiers[1],
            self.constant.tiers[2],
        ]));
        for symbol in sorted(self.cells.keys()) {
            weight = self.cells[symbol];
            copy.cells[symbol] = LexWeight(tiers=[
                weight.tiers[0], weight.tiers[1], weight.tiers[2],
            ]);
        }
        return copy;
    }

    def substitute(symbol: int, row: Row) -> None {
        coefficient = self.cells.get(symbol);
        if coefficient is None {
            return;
        }
        self.cells.pop(symbol);
        self.insert_row(row, coefficient);
    }
}


obj MutationJournal {
    has id_tick_start: int = 0,
        # Symbol ids created during this operation.
        allocated_symbols: list[int] = [],
        # External variable ids registered during this operation.
        new_var_ids: list[int] = [],
        # Row keys inserted during this operation (did not exist before).
        inserted_rows: list[int] = [],
        # Pre-mutation deep copies of pre-existing touched rows.
        row_snapshots: dict[int, Row] = {},
        # Pre-mutation copy of the lexicographic objective, when touched.
        objective_snapshot: CostRow | None = None,
        # Length of the infeasible-row worklist before this operation.
        infeasible_start: int = 0;
}


obj StoredConstraint {
    has expression: Expression,
        relation: Relation,
        strength: StrengthTier = StrengthTier.REQUIRED,
        provenance: str = "",
        content_key: str = "";
}


obj EditInfo {
    has var_id: int,
        key: str,
        handle: ConstraintHandle,
        constant: float = 0.0;
}

