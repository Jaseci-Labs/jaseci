"""Cell quantization: solved floats -> coherent terminal-cell edges.

LAYOUT-ENGINE-PLAN §7.2 (locked policy):

- viewport edges are exact integers (callers pass them as ints);
- values within EPSILON of an integer snap to that integer;
- other unconstrained edges round to nearest integer, with exact halves
  toward the smaller coordinate (floor wins ties);
- required-equal edge expressions are grouped and snapped once for the
  group (snap_edge_group);
- flow partitions use largest remainder: floor each flexible child's
  continuous target, then distribute the remaining cells one each by
  descending fractional remainder, with ordered Child.rank and then jid
  as ties — the CALLER passes children already in rank/jid order, so
  this module breaks ties by ascending index;
- fixed integer claims remain fixed;
- for a bounded flexible child, integer validation uses ceil(minimum)
  and floor(maximum); a bound interval containing no integer cell size
  is rejected;
- after partition quantization every flexible child differs from its
  continuous target by less than one cell and child sizes sum exactly
  to the integer parent span;
- derived width/height are computed by callers as end_cell - start_cell,
  never rounded independently;
- negative derived sizes are an internal invariant failure;
- clips are computed AFTER quantization (M5's job).

M5 INTEGRATION CONTRACT (overflow partitions): quantize_partition
requires an exact integer closure on span. A partition whose REQUIRED
FIXED claims exceed the parent span compiles solvable-with-warning
(closing edge omitted, children stick out past the parent end), so it
has NO honest integer partition and MUST NOT be handed here. The M5
publisher handles those partitions clip-aware: quantize each child's
edges independently (snap_edge), keep sizes as compiled, let frame
validation clip against the parent box, and attach the OVERFLOW warning
to the published frame. Only non-overflow partitions go through
quantize_partition. This seam is deliberate; do not "fix" by relaxing
the closure requirement.

This module is pure: constraints.algebra constants only, no OSP types,
no UI types, no solver, no measurement.
"""

# EPSILON mirrors constraints.algebra's 1e-8 (verified equal at import time
# below); a direct import feeds native compares from a server-placed global,
# which cannot cross the boundary. Keep in sync if algebra's constant moves.
glob:priv EPSILON: float = 1e-8;



# Bounds sentinels for PartitionRequest.minimums/maximums (full-length
# parallel lists; entries at the sentinels mean "unbounded" on that side).
glob _NO_MIN: float = -1e308;
glob _NO_MAX: float = 1e308;


"""Largest-remainder request for one flow partition along one axis."""
obj PartitionRequest {
    has span: int,
        # Continuous target per child, in rank/jid order.
        targets: list[float],
        # True where the child's claim is a FIXED integer (never grows
        # or shrinks during distribution).
        fixed: list[bool] = [],
        # Optional integer-validity bounds; either empty (no checking)
        # or full length matching targets.
        minimums: list[float] = [],
        maximums: list[float] = [];
}


"""Quantization outcome. On ok=False sizes is empty and `index` names
the offending child when one exists (-1 for structural failures like
span exhaustion)."""
obj QuantizeResult {
    has ok: bool = True,
        sizes: list[int] = [],
        message: str = "",
        index: int = -1;
}


def _floor(value: float) -> int {
    t = int(value);
    if value >= 0.0 or float(t) == value {
        return t;
    }
    return t - 1;
}


def _ceil(value: float) -> int {
    neg = -value;
    f = _floor(neg);
    return -f;
}


"""§7.2 edge snap: EPSILON-close integers win; otherwise nearest
integer with exact halves toward the smaller coordinate."""
def snap_edge(value: float) -> int {
    fl = _floor(value);
    frac = value - float(fl);
    if frac < EPSILON {
        return fl;
    }
    if frac > 1.0 - EPSILON {
        return fl + 1;
    }
    if frac > 0.5 {
        return fl + 1;
    }
    return fl;  # Exact halves land here: toward the smaller coordinate.
}


"""Snap a group of REQUIRED-equal edge expressions once.

All members receive the representative's snapped value; members are
expected to be within float noise of each other (they compile to one
equation). Deliberately does not fail on drift — grouping exists to make
noise irrelevant."""
def snap_edge_group(values: list[float]) -> list[int] {
    rep = snap_edge(values[0]);
    out: list[int] = [];
    for _v in values {
        out.append(rep);
    }
    return out;
}


def _quant_fail(message: str, index: int) -> QuantizeResult {
    return QuantizeResult(ok=False, message=message, index=index);
}


def _bounds_ok_shape(req: PartitionRequest) -> bool {
    n = len(req.targets);
    if len(req.fixed) != 0 and len(req.fixed) != n {
        return False;
    }
    if len(req.minimums) != 0 and len(req.minimums) != n {
        return False;
    }
    if len(req.maximums) != 0 and len(req.maximums) != n {
        return False;
    }
    return True;
}


"""§7.2 largest-remainder quantization of one sibling partition.

`req.targets` must be in rank/jid order — ties in the remainder race
resolve by ascending index, which is exactly the plan's rank-then-jid
rule under that precondition."""
def quantize_partition(req: PartitionRequest) -> QuantizeResult {
    if not _bounds_ok_shape(req) or req.span < 0 {
        return _quant_fail("malformed partition request", -1);
    }
    n = len(req.targets);
    if n == 0 {
        if req.span != 0 {
            return _quant_fail("nonempty span with no children", -1);
        }
        return QuantizeResult(ok=True);
    }

    fixed_flags: list[bool] = [];
    if len(req.fixed) == 0 {
        for _i in range(n) {
            fixed_flags.append(False);
        }
    } else {
        for f in req.fixed {
            fixed_flags.append(f);
        }
    }

    sizes: list[int] = [0] * n;
    floors: list[int] = [0] * n;
    remainders: list[float] = [0.0] * n;
    fixed_sum = 0;

    for i in range(n) {
        t = req.targets[i];
        if t < 0.0 {
            return _quant_fail("negative continuous target", i);
        }
        if fixed_flags[i] {
            sizes[i] = snap_edge(t);
            fixed_sum += sizes[i];
        } else {
            floors[i] = _floor(t);
            remainders[i] = t - float(floors[i]);
            # Flexible children START at their floored target; the
            # remainder race then awards whole extra cells on top.
            sizes[i] = floors[i];
        }
    }

    leftover = req.span - fixed_sum;
    for i in range(n) {
        if not fixed_flags[i] {
            leftover -= floors[i];
        }
    }

    # Overflow path: flexible floors cannot cover the deficit once
    # clamped at zero; report rather than fabricate negative sizes.
    if leftover < 0 {
        recoverable = True;
        for i in range(n) {
            if not fixed_flags[i] and floors[i] > 0 {
                recoverable = False;
            }
        }
        if recoverable {
            return _quant_fail(
                "fixed integer claims exceed parent span", -1
            );
        }
        return _quant_fail(
            "flexible floors exceed remaining span under largest-remainder policy", -1
        );
    }

    flexible: list[int] = [];
    for i in range(n) {
        if not fixed_flags[i] {
            flexible.append(i);
        }
    }
    if 0 < len(flexible) < 3 {
        # Plan §8.3 approved-correction scope: largest remainder applies
        # only to partitions with three or more fractional grow targets.
        # Below that, legacy parity rules — every leftover cell goes to
        # the final flexible child (int shares, remainder to last).
        sizes[flexible[len(flexible) - 1]] += leftover;
        leftover = 0;
    }

    # Largest-remainder distribution: one cell at a time to the highest
    # remaining fraction; receiving a cell consumes one unit of fraction,
    # so ties naturally fall through to the next-lowest index.
    while leftover > 0 and len(flexible) {
        best = -1;
        for i in flexible {
            if best == -1 or remainders[i] > remainders[best] + EPSILON {
                best = i;
            }
        }
        sizes[best] += 1;
        remainders[best] -= 1.0;
        leftover -= 1;
    }

    res = _apply_bounds(req, sizes, flexible, remainders);
    return res;
}


"""Integer-validity pass: ceil(min)/floor(max) emptiness rejection plus
a bounded number of clamp-and-redistribute repairs to restore exact
partition closure after a bound clamp moves cells.

`remainders` carries the POST-distribution fractional state from the
distribution loop, so repair moves respect the same ordering policy.

Bounds are deliberately IGNORED for FIXED children: an explicit size
beats every other policy (same rule as cross-axis STRETCH losing to
FIXED), so their requests never enter imin/imax. Do not add them there
without revisiting that decision."""
def _apply_bounds(
    req: PartitionRequest,
    sizes: list[int],
    flexible: list[int],
    remainders: list[float],
) -> QuantizeResult {
    if len(req.minimums) == 0 and len(req.maximums) == 0 {
        if sum(sizes) != req.span {
            return _quant_fail("partition does not close on span", -1);
        }
        for i in range(len(sizes)) {
            if sizes[i] < 0 {
                return _quant_fail("negative derived size", i);
            }
        }
        return QuantizeResult(ok=True, sizes=sizes);
    }

    imin: list[int] = [];
    imax: list[int] = [];
    for i in range(len(req.targets)) {
        mn = _NO_MIN;
        mx = _NO_MAX;
        if len(req.minimums) != 0 {
            mn = req.minimums[i];
        }
        if len(req.maximums) != 0 {
            mx = req.maximums[i];
        }
        lo = _ceil(mn);
        hi = _floor(mx);
        if lo > hi {
            return _quant_fail(
                "bound interval contains no integer cell size", i
            );
        }
        imin.append(lo);
        imax.append(hi);
    }

    # Clamp violators, then repair closure by moving whole cells between
    # flexible children. Bounded iterations; structural failure if the
    # repair cannot converge (should be impossible after freeze-at-bound
    # allocation upstream, and we want loud failure over silent drift).
    for _round in range(8) {
        delta = 0;
        clamped: list[int] = [];
        for i in flexible {
            if sizes[i] < imin[i] {
                # Clamping UP adds cells: the partition now has surplus
                # to remove elsewhere.
                delta -= imin[i] - sizes[i];
                sizes[i] = imin[i];
                clamped.append(i);
            } elif sizes[i] > imax[i] {
                # Clamping DOWN removes cells: deficit to refill.
                delta += sizes[i] - imax[i];
                sizes[i] = imax[i];
                clamped.append(i);
            }
        }
        if delta == 0 {
            break;
        }
        # Move `delta` cells into (positive) or out of (negative) the
        # flexible set EXCLUDING children clamped this round — they sit
        # exactly on their bound and moving them would just oscillate.
        # Largest/smallest post-distribution remainder first.
        movable: list[int] = [];
        for i in flexible {
            is_clamped = False;
            for c in clamped {
                if c == i {
                    is_clamped = True;
                }
            }
            if not is_clamped {
                movable.append(i);
            }
        }
        steps = abs(delta);
        for _s in range(steps) {
            best = -1;
            for i in movable {
                if delta > 0 and imax[i] - sizes[i] <= 0 {
                    continue;  # No headroom.
                }
                if delta < 0 and sizes[i] - imin[i] <= 0 {
                    continue;  # Nothing to give.
                }
                if best == -1 {
                    best = i;
                    continue;
                }
                if delta > 0 and remainders[i] > remainders[best] {
                    best = i;
                }
                if delta < 0 and remainders[i] < remainders[best] {
                    best = i;
                }
            }
            if best == -1 {
                return _quant_fail(
                    "bound repair could not restore closure", -1
                );
            }
            if delta > 0 {
                sizes[best] += 1;
            } else {
                sizes[best] -= 1;
            }
        }
        if not clamped {
            break;
        }
    }
    if sum(sizes) != req.span {
        return _quant_fail("partition does not close on span", -1);
    }
    for i in range(len(sizes)) {
        if sizes[i] < 0 {
            return _quant_fail("negative derived size", i);
        }
    }
    return QuantizeResult(ok=True, sizes=sizes);
}
