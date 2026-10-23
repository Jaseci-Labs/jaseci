"""D22 layout authoring vocabulary over the pure constraint algebra.

This module deliberately has no UI or graph-node dependency. A caller owns
node identity and supplies four deterministic Variables per node:
left (x), top (y), width, and height. Relations are ordinary Constraint
values, so pattern helpers are transparent and leave no persistent state.

The coordinate convention is terminal-style: left/top are the origin and
right = left + width, bottom = top + height.
"""

import from .algebra {
    Constraint,
    Expression,
    Relation,
    StrengthTier,
    Term,
    Variable,
    normalize_expression,
}


"""Derive a node's four variables from a caller-owned base id.

The ids are base_id, base_id+1, base_id+2, and base_id+3 for left, top,
width, and height. Right and bottom are affine expressions, not variables.
Callers must choose non-overlapping base-id ranges for distinct nodes.
"""
def node_vars(base_id: int) -> dict[str, Variable] {
    return {
        "left": Variable(id=base_id),
        "top": Variable(id=base_id + 1),
        "width": Variable(id=base_id + 2),
        "height": Variable(id=base_id + 3),
    };
}


def _term(v: Variable, coefficient: float = 1.0) -> Term {
    return Term(variable=v, coefficient=coefficient);
}


def _constraint(
    terms: list[Term],
    constant: float = 0.0,
    relation: Relation = Relation.EQ,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> Constraint {
    return Constraint(
        expression=normalize_expression(
            Expression(terms=terms, constant=constant)
        ),
        relation=relation,
        strength=strength,
    );
}


"""Raw affine escape hatch. The expression is normalized on construction."""
def affine_constraint(
    expression: Expression,
    relation: Relation = Relation.EQ,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> Constraint {
    return Constraint(
        expression=normalize_expression(expression),
        relation=relation,
        strength=strength,
    );
}


"""source bottom + gap == target top; source is above target."""
def above(
    source: dict[str, Variable],
    target: dict[str, Variable],
    gap: float = 0.0,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint([
        _term(source["top"]),
        _term(source["height"]),
        _term(target["top"], -1.0),
    ], constant=gap, strength=strength)];
}


"""source top == target bottom + gap; source is below target."""
def below(
    source: dict[str, Variable],
    target: dict[str, Variable],
    gap: float = 0.0,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint([
        _term(source["top"]),
        _term(target["top"], -1.0),
        _term(target["height"], -1.0),
    ], constant=-gap, strength=strength)];
}


"""source right + gap == target left; source is left of target."""
def left_of(
    source: dict[str, Variable],
    target: dict[str, Variable],
    gap: float = 0.0,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint([
        _term(source["left"]),
        _term(source["width"]),
        _term(target["left"], -1.0),
    ], constant=gap, strength=strength)];
}


"""source left == target right + gap; source is right of target."""
def right_of(
    source: dict[str, Variable],
    target: dict[str, Variable],
    gap: float = 0.0,
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint([
        _term(source["left"]),
        _term(target["left"], -1.0),
        _term(target["width"], -1.0),
    ], constant=-gap, strength=strength)];
}


"""source left == target left; alignment is a STRONG user-intent fact."""
def align_left(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["left"]),
        _term(target["left"], -1.0),
    ], strength=strength)];
}


"""source right == target right; alignment is STRONG by default."""
def align_right(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["left"]),
        _term(source["width"]),
        _term(target["left"], -1.0),
        _term(target["width"], -1.0),
    ], strength=strength)];
}


"""source top == target top; alignment is STRONG by default."""
def align_top(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["top"]),
        _term(target["top"], -1.0),
    ], strength=strength)];
}


"""source bottom == target bottom; alignment is STRONG by default."""
def align_bottom(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["top"]),
        _term(source["height"]),
        _term(target["top"], -1.0),
        _term(target["height"], -1.0),
    ], strength=strength)];
}


"""source and target horizontal centers coincide."""
def center_x(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["left"]),
        _term(source["width"], 0.5),
        _term(target["left"], -1.0),
        _term(target["width"], -0.5),
    ], strength=strength)];
}


"""source and target vertical centers coincide."""
def center_y(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["top"]),
        _term(source["height"], 0.5),
        _term(target["top"], -1.0),
        _term(target["height"], -0.5),
    ], strength=strength)];
}


"""source left == target left and source right == target right."""
def fill_width(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    result: list[Constraint] = [];
    result.extend(align_left(source, target, strength));
    result.extend(align_right(source, target, strength));
    return result;
}


"""source top == target top and source bottom == target bottom."""
def fill_height(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    result: list[Constraint] = [];
    result.extend(align_top(source, target, strength));
    result.extend(align_bottom(source, target, strength));
    return result;
}


"""source width == target width; STRONG by default."""
def same_width(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["width"]),
        _term(target["width"], -1.0),
    ], strength=strength)];
}


"""source height == target height; STRONG by default."""
def same_height(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return [_constraint([
        _term(source["height"]),
        _term(target["height"], -1.0),
    ], strength=strength)];
}


"""width >= 0 is a REQUIRED geometric invariant."""
def width_nonnegative(
    layout_node: dict[str, Variable],
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint(
        [_term(layout_node["width"])],
        relation=Relation.GEQ,
        strength=strength,
    )];
}


"""height >= 0 is a REQUIRED geometric invariant."""
def height_nonnegative(
    layout_node: dict[str, Variable],
    strength: StrengthTier = StrengthTier.REQUIRED,
) -> list[Constraint] {
    return [_constraint(
        [_term(layout_node["height"])],
        relation=Relation.GEQ,
        strength=strength,
    )];
}


"""Preferred width is a WEAK size preference, not a hard geometry fact."""
def preferred_width(
    layout_node: dict[str, Variable],
    preferred: float,
    strength: StrengthTier = StrengthTier.WEAK,
) -> list[Constraint] {
    return [_constraint(
        [_term(layout_node["width"])],
        constant=-preferred,
        strength=strength,
    )];
}


"""Preferred height is a WEAK size preference, not a hard geometry fact."""
def preferred_height(
    layout_node: dict[str, Variable],
    preferred: float,
    strength: StrengthTier = StrengthTier.WEAK,
) -> list[Constraint] {
    return [_constraint(
        [_term(layout_node["height"])],
        constant=-preferred,
        strength=strength,
    )];
}


"""Stack children top-to-bottom inside parent.

The first child shares the parent's top edge; each following child is below
its predecessor by gap. With fill=true every child also fills the parent's
width. Expansion consists solely of ordinary constraints in deterministic
order: anchor, inter-child edges, then optional fill constraints.
"""
def vertical_flow(
    parent: dict[str, Variable],
    children: list[dict[str, Variable]],
    gap: float = 0.0,
    fill: bool = False,
) -> list[Constraint] {
    result: list[Constraint] = [];
    if len(children) == 0 {
        return result;
    }
    result.extend(align_top(children[0], parent, StrengthTier.REQUIRED));
    for i in range(1, len(children)) {
        result.extend(above(children[i - 1], children[i], gap));
    }
    if fill {
        for child in children {
            result.extend(fill_width(child, parent));
        }
    }
    return result;
}


"""Stack children left-to-right inside parent, optionally filling height."""
def horizontal_flow(
    parent: dict[str, Variable],
    children: list[dict[str, Variable]],
    gap: float = 0.0,
    fill: bool = False,
) -> list[Constraint] {
    result: list[Constraint] = [];
    if len(children) == 0 {
        return result;
    }
    result.extend(align_left(children[0], parent, StrengthTier.REQUIRED));
    for i in range(1, len(children)) {
        result.extend(left_of(children[i - 1], children[i], gap));
    }
    if fill {
        for child in children {
            result.extend(fill_height(child, parent));
        }
    }
    return result;
}


"""Readable aliases for the two flow patterns."""
def column(
    parent: dict[str, Variable],
    children: list[dict[str, Variable]],
    gap: float = 0.0,
    fill: bool = False,
) -> list[Constraint] {
    return vertical_flow(parent, children, gap, fill);
}


def row(
    parent: dict[str, Variable],
    children: list[dict[str, Variable]],
    gap: float = 0.0,
    fill: bool = False,
) -> list[Constraint] {
    return horizontal_flow(parent, children, gap, fill);
}


# Naming aliases matching the prose vocabulary.
def align_center_x(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return center_x(source, target, strength);
}


def align_center_y(
    source: dict[str, Variable],
    target: dict[str, Variable],
    strength: StrengthTier = StrengthTier.STRONG,
) -> list[Constraint] {
    return center_y(source, target, strength);
}
