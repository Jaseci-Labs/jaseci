"""Behavior tests for the permanent layout seam (LAYOUT-ENGINE-PLAN §4/§7).

Registry lifecycle (spec validation, relation lifecycle, content
revisions, clearing) and the compute_layout pipeline (legacy-parity
shell geometry, atomic publication, generation monotonicity, resize
reclamping, scroll clamping, overlay centering, wrap-driven heights,
degenerate viewports, measurement-cache invalidation).

Both suites moved here at the M6 cutover: their functions live in
ui/layout.jac and this module shares its stem.
"""

# Same-stem note: only functions DECLARED in ui.layout (compute_layout)
# are ambient here; never import from ui.layout inside this module
# (circular import at collection). Everything else — value types and the
# registry lifecycle — comes from the leaf module ui.layout_types.

import from ..constraints.algebra {
    StrengthTier,
}
import from .layout_types {
    Axis,
    AxisSize,
    LayoutError,
    LayoutFrame,
    LayoutRelation,
    LayoutRelationKind,
    LayoutResult,
    LayoutSpec,
    LayoutState,
    MutationResult,
    Rect,
    RelationHandle,
    Size,
    SizeMode,
    Viewport,
    add_relation,
    clear_node,
    create_layout_state,
    frame_entry_of,
    rect_of,
    remove_relation,
    set_content,
    set_scroll_offset,
    set_spec,
    validate_spec,
}
import from .model {
    ApprovalOverlay,
    Child,
    Header,
    Layer,
    MainScreen,
    Prompt,
    Status,
    TranscriptView,
    node_id,
}


# ----------------------------------------------------------------------
# Shared helpers.
# ----------------------------------------------------------------------

def _fixed(n: float) -> AxisSize {
    return AxisSize(mode=SizeMode.FIXED, preferred=n);
}


def _fill() -> AxisSize {
    return AxisSize(mode=SizeMode.FILL);
}


def _grow(weight: float) -> AxisSize {
    return AxisSize(mode=SizeMode.GROW, grow_weight=weight);
}


# ----------------------------------------------------------------------
# Registry lifecycle tests.
# ----------------------------------------------------------------------

def _intrinsic() -> AxisSize {
    return AxisSize(mode=SizeMode.INTRINSIC);
}


def _spec(width: AxisSize = _fixed(40), height: AxisSize = _fixed(3)) -> LayoutSpec {
    return LayoutSpec(width=width, height=height);
}


def _must_handle(r: MutationResult) -> RelationHandle {
    assert r.relation_handle is not None;
    return r.relation_handle;
}


def _rel(
    owner: str,
    source: str,
    target: str,
    kind: LayoutRelationKind,
    axis: Axis,
) -> LayoutRelation {
    return LayoutRelation(
        owner_id=owner,
        source_id=source,
        target_id=target,
        kind=kind,
        axis=axis,
        provenance="test",
    );
}


test "set_spec registers a validated spec by stable node id" {
    state = create_layout_state(100, 40);
    assert state.viewport.columns == 100;
    prompt = Prompt(key="p");
    r = set_spec(state, prompt, _spec());
    assert r.ok;
    assert node_id(prompt) in state.specs;

    # Replacing the spec is allowed; last write wins.
    r2 = set_spec(state, prompt, _spec(height=_fixed(5)));
    assert r2.ok;
    assert state.specs[node_id(prompt)].height.preferred == 5.0;
}


test "set_spec rejects malformed specs with INVALID_SPEC" {
    state = create_layout_state();
    status = Status(key="s");

    cases: list[LayoutSpec] = [
        # Negative minimum.
        _spec(width=AxisSize(mode=SizeMode.BOUNDED, minimum=-1.0)),
        # minimum > maximum.
        _spec(width=AxisSize(
            mode=SizeMode.BOUNDED,
            minimum=10.0,
            maximum=5.0,
        )),
        # FIXED without preferred.
        _spec(width=AxisSize(mode=SizeMode.FIXED)),
        # GROW with zero weight.
        _spec(width=AxisSize(mode=SizeMode.GROW, grow_weight=0.0)),
    ];
    for bad in cases {
        r = set_spec(state, status, bad);
        assert not r.ok;
        assert len(r.diagnostics) == 1;
        assert r.diagnostics[0].code == LayoutError.INVALID_SPEC;
    }
    assert len(state.specs) == 0;
}


test "validate_spec reports non-finite bounds" {
    spec = _spec(width=AxisSize(
        mode=SizeMode.BOUNDED,
        minimum=float("nan"),
        maximum=float("inf"),
    ));
    diags = validate_spec(spec, "x");
    assert len(diags) >= 1;
    assert diags[0].code == LayoutError.INVALID_SPEC;
}


test "add_relation validates liveness, shape, and gap rules" {
    state = create_layout_state();
    header = Header(key="h");
    transcript = TranscriptView(key="t");
    set_spec(state, header, _spec());
    set_spec(state, transcript, _spec());

    # Unregistered endpoints are stale.
    ghost = _rel(node_id(header), node_id(transcript), "ghost",
                 LayoutRelationKind.LEFT_OF, Axis.HORIZONTAL);
    r0 = add_relation(state, ghost);
    assert not r0.ok;
    assert r0.diagnostics[0].code == LayoutError.STALE_NODE;
    assert r0.diagnostics[0].node_ids == ["ghost"];

    # Directional kind on the wrong axis.
    wrong_axis = _rel(node_id(header), node_id(header), node_id(transcript),
                      LayoutRelationKind.LEFT_OF, Axis.VERTICAL);
    r1 = add_relation(state, wrong_axis);
    assert not r1.ok;
    assert r1.diagnostics[0].code == LayoutError.INVALID_RELATION;

    # Negative gap.
    neg_gap = _rel(node_id(header), node_id(header), node_id(transcript),
                   LayoutRelationKind.LEFT_OF, Axis.HORIZONTAL);
    neg_gap.gap = -1.0;
    r2 = add_relation(state, neg_gap);
    assert not r2.ok;
    assert r2.diagnostics[0].code == LayoutError.INVALID_RELATION;

    # Alignment kind with nonzero gap.
    aligned = _rel(node_id(header), node_id(header), node_id(transcript),
                   LayoutRelationKind.ALIGN_START, Axis.HORIZONTAL);
    aligned.gap = 2.0;
    r3 = add_relation(state, aligned);
    assert not r3.ok;
    assert r3.diagnostics[0].code == LayoutError.INVALID_RELATION;

    # Happy path allocates deterministic ascending handles.
    good = _rel(node_id(header), node_id(header), node_id(transcript),
                LayoutRelationKind.ALIGN_START, Axis.HORIZONTAL);
    r4 = add_relation(state, good);
    assert r4.ok;
    assert r4.relation_handle is not None;
    assert r4.relation_handle.id == 1;
    assert len(state.relations) == 1;
}


test "duplicate relations merge provenance or reject strength change" {
    state = create_layout_state();
    a = Header(key="a");
    b = TranscriptView(key="b");
    set_spec(state, a, _spec());
    set_spec(state, b, _spec());

    first = _rel(node_id(a), node_id(a), node_id(b),
                 LayoutRelationKind.SAME_SIZE, Axis.HORIZONTAL);
    first.provenance = "shell:header";
    r1 = add_relation(state, first);
    assert r1.ok;

    second = _rel(node_id(a), node_id(a), node_id(b),
                  LayoutRelationKind.SAME_SIZE, Axis.HORIZONTAL);
    second.provenance = "gate:duplicate";
    r2 = add_relation(state, second);
    assert r2.ok;
    # Merged into one stored relation carrying both provenances.
    assert len(state.relations) == 1;
    merged = state.relations[_must_handle(r1).id];
    assert merged.provenance == "shell:header;gate:duplicate";

    # Same expression, different strength -> rejected.
    third = _rel(node_id(a), node_id(a), node_id(b),
                 LayoutRelationKind.SAME_SIZE, Axis.HORIZONTAL);
    third.strength = StrengthTier.STRONG;
    third.provenance = "gate:conflict";
    r3 = add_relation(state, third);
    assert not r3.ok;
    assert r3.diagnostics[0].code == LayoutError.INVALID_RELATION;
}


test "remove_relation drops exactly its handle" {
    state = create_layout_state();
    a = Header(key="a");
    b = TranscriptView(key="b");
    set_spec(state, a, _spec());
    set_spec(state, b, _spec());

    missing = remove_relation(state, RelationHandle(id=99));
    assert not missing.ok;

    rel = _rel(node_id(a), node_id(a), node_id(b),
               LayoutRelationKind.ABOVE, Axis.VERTICAL);
    r = add_relation(state, rel);
    assert r.ok;
    handle = _must_handle(r);
    assert remove_relation(state, handle).ok;
    assert len(state.relations) == 0;
    assert not remove_relation(state, handle).ok;
}


test "set_content enforces monotonic revisions and liveness" {
    state = create_layout_state();
    t = TranscriptView(key="t");
    set_spec(state, t, _spec());

    ghost = set_content(state, Status(key="nope"), ["x"], 1);
    assert not ghost.ok;
    assert ghost.diagnostics[0].code == LayoutError.STALE_NODE;

    assert set_content(state, t, ["one"], 1).ok;
    # Decreasing either revision is rejected.
    assert not set_content(state, t, ["two"], 0).ok;
    assert not set_content(state, t, ["two"], 1, style_revision=-1).ok;
    # Equal-or-advancing revisions replace content.
    assert set_content(state, t, ["two"], 1).ok;
    assert set_content(state, t, ["three"], 2).ok;
    ent = state.content[node_id(t)];
    assert ent.lines == ["three"];
    assert ent.content_revision == 2;
}


test "clear_node removes spec, content, and incident relations atomically" {
    state = create_layout_state();
    owner_node = Header(key="owner");
    left = TranscriptView(key="left");
    right = Status(key="right");
    set_spec(state, owner_node, _spec());
    set_spec(state, left, _spec());
    set_spec(state, right, _spec());
    assert set_content(state, left, ["l"], 1).ok;

    # left --ABOVE--> right (owned by root), and left --SAME_SIZE--> root.
    r1 = add_relation(state, _rel(
        node_id(owner_node), node_id(left), node_id(right),
        LayoutRelationKind.ABOVE, Axis.VERTICAL,
    ));
    r2 = add_relation(state, _rel(
        node_id(owner_node), node_id(left), node_id(owner_node),
        LayoutRelationKind.SAME_SIZE, Axis.HORIZONTAL,
    ));
    assert r1.ok and r2.ok;
    assert len(state.relations) == 2;

    assert clear_node(state, left).ok;
    assert node_id(left) not in state.specs;
    assert node_id(left) not in state.content;
    assert len(state.relations) == 0;
    # Untouched nodes survive.
    assert node_id(owner_node) in state.specs;
    assert node_id(right) in state.specs;
}


test "frame accessors are None before first publication" {
    state = create_layout_state();
    p = Prompt(key="p");
    set_spec(state, p, _spec());
    assert frame_entry_of(state, p) is None;
    assert rect_of(state, p) is None;
}


# ----------------------------------------------------------------------
# compute_layout pipeline tests.
# ----------------------------------------------------------------------

def _published(state: LayoutState) -> LayoutFrame {
    f = state.last_frame;
    if f is None {
        raise ValueError("expected a published frame");
    }
    return f;
}


obj _ShellFixture {
    has state: LayoutState,
        screen: MainScreen,
        header: Header,
        transcript: TranscriptView,
        status: Status,
        prompt: Prompt;
}


def _shell(columns: int = 80, rows: int = 24) -> _ShellFixture {
    screen = MainScreen(key="main");
    header = Header(key="header");
    transcript = TranscriptView(key="transcript");
    status = Status(key="status");
    prompt = Prompt(key="prompt");
    screen +>:Child(rank=1024):+> header;
    screen +>:Child(rank=2048):+> transcript;
    screen +>:Child(rank=3072):+> status;
    screen +>:Child(rank=4096):+> prompt;

    state = create_layout_state(columns, rows);
    set_spec(state, screen, LayoutSpec(width=_fill(), height=_fill()));
    set_spec(state, header, LayoutSpec(width=_fill(), height=_fixed(1.0)));
    set_spec(
        state,
        transcript,
        LayoutSpec(width=_fill(), height=_grow(1.0), scroll_vertical=True),
    );
    set_spec(state, status, LayoutSpec(width=_fill(), height=_fixed(1.0)));
    set_spec(state, prompt, LayoutSpec(width=_fill(), height=_fixed(2.0)));
    set_content(state, header, ["Osprey"], 1);
    set_content(state, status, ["ready"], 1);
    set_content(state, prompt, ["> "], 1);
    return _ShellFixture(
        state=state,
        screen=screen,
        header=header,
        transcript=transcript,
        status=status,
        prompt=prompt,
    );
}


test "pipeline reproduces legacy-parity shell geometry at 80x24" {
    m = _shell();
    r = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r.ok;
    assert r.frame is not None;

    hid = node_id(m.header);
    tid = node_id(m.transcript);
    sid = node_id(m.status);
    pid = node_id(m.prompt);

    fh = r.frame.entries[hid];
    assert fh.rect.x == 0;
    assert fh.rect.y == 0;
    assert fh.rect.width == 80;
    assert fh.rect.height == 1;

    ft = r.frame.entries[tid];
    assert ft.rect.y == 1;
    assert ft.rect.height == 20;
    assert ft.rect.width == 80;
    assert ft.measured.width == 80;
    assert ft.measured.height == 20;

    fs = r.frame.entries[sid];
    assert fs.rect.y == 21;
    assert fs.rect.height == 1;

    fp = r.frame.entries[pid];
    assert fp.rect.y == 22;
    assert fp.rect.height == 2;

    # Partition closure: children exactly fill the column.
    assert (
        fh.rect.height + ft.rect.height
        + fs.rect.height + fp.rect.height
    ) == 24;

    # Clips nest inside the viewport.
    assert ft.clip.width <= 80;
    assert ft.clip.height <= 20;

    assert r.frame.generation == 1;
    assert r.frame.overlay_ids == [];
}


test "publication replaces state.last_frame and generations advance" {
    m = _shell();
    r1 = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r1.ok;
    assert m.state.last_frame is not None;
    assert _published(m.state).generation == 1;

    r2 = compute_layout(m.state, m.screen, Viewport(columns=100, rows=30));
    assert r2.ok;
    assert _published(m.state).generation == 2;
    assert _published(m.state).viewport.columns == 100;

    # Transcript reclamped into the resized column.
    tid = node_id(m.transcript);
    e = _published(m.state).entries[tid];
    assert e.rect.height == 26;
    assert e.rect.width == 100;
}


test "failed run leaves the prior published frame untouched" {
    m = _shell();
    r1 = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r1.ok;
    published = m.state.last_frame;

    # A scoped node without a spec aborts compilation.
    stranger = Prompt(key="stranger");
    m.screen +>:Child(rank=9999):+> stranger;

    r2 = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert not r2.ok;
    assert len(r2.diagnostics) >= 1;
    assert m.state.last_frame is published;
    assert _published(m.state).generation == 1;
}


test "scroll offset clamps to wrapped height minus visible rows" {
    m = _shell();
    lines: list[str] = [];
    for i in range(50) {
        lines.append("line " + str(i));
    }
    set_content(m.state, m.transcript, lines, 1);
    set_scroll_offset(m.state, m.transcript, 500);

    r = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r.ok;
    tid = node_id(m.transcript);
    e = _published(m.state).entries[tid];
    assert e.requested_scroll_offset == 500;
    assert e.max_scroll_offset == len(e.wrapped_lines) - 20;
    assert e.scroll_offset == e.max_scroll_offset;
}


test "wrapped content drives wrapped lines while fixed height clips" {
    m = _shell();
    long_line = "";
    for i in range(30) {
        long_line = long_line + "word ";
    }
    set_content(m.state, m.header, [long_line], 1);

    r = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r.ok;
    hid = node_id(m.header);
    e = _published(m.state).entries[hid];
    assert e.rect.width == 80;
    # Content wraps at the quantized integer width...
    assert len(e.wrapped_lines) >= 2;
    # ...but the FIXED height still wins: overflow is clipped, not sized.
    assert e.measured.height == 1;
    assert e.clip.height <= 1;
}


test "centered fixed overlay lands at integer floor division" {
    screen = MainScreen(key="main");
    overlay = ApprovalOverlay(key="ov");
    screen +>:Layer(z_index=10, modal=True):+> overlay;

    state = create_layout_state(80, 24);
    set_spec(state, screen, LayoutSpec(width=_fill(), height=_fill()));
    set_spec(
        state,
        overlay,
        LayoutSpec(width=_fixed(20.0), height=_fixed(6.0)),
    );

    r = compute_layout(state, screen, Viewport(columns=80, rows=24));
    assert r.ok;
    oid = node_id(overlay);
    e = _published(state).entries[oid];
    assert e.rect.x == 30;  # (80 - 20) // 2
    assert e.rect.y == 9;   # (24 - 6) // 2
    assert e.rect.width == 20;
    assert e.rect.height == 6;
    assert _published(state).overlay_ids == [oid];
}


test "oversized fixed overlay keeps size and clips to viewport" {
    screen = MainScreen(key="main");
    overlay = ApprovalOverlay(key="big");
    screen +>:Layer(z_index=10, modal=True):+> overlay;

    state = create_layout_state(80, 24);
    set_spec(state, screen, LayoutSpec(width=_fill(), height=_fill()));
    set_spec(
        state,
        overlay,
        LayoutSpec(width=_fixed(120.0), height=_fixed(40.0)),
    );

    r = compute_layout(state, screen, Viewport(columns=80, rows=24));
    assert r.ok;
    e = _published(state).entries[node_id(overlay)];
    assert e.rect.width == 120;
    assert e.rect.height == 40;
    assert e.rect.x == 0;  # origin clamped
    assert e.rect.y == 0;
}


test "degenerate viewports stay satisfiable" {
    m = _shell();
    for vp in [Viewport(columns=0, rows=0), Viewport(columns=1, rows=1)] {
        r = compute_layout(m.state, m.screen, vp);
        assert r.ok;
        root_e = _published(m.state).entries[node_id(m.screen)];
        assert root_e.rect.width == vp.columns;
        assert root_e.rect.height == vp.rows;
    }
}


test "content revision bump rewraps through the measure cache" {
    m = _shell();
    set_content(m.state, m.transcript, ["short"], 1);
    r1 = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r1.ok;
    tid = node_id(m.transcript);
    e1 = _published(m.state).entries[tid];
    assert len(e1.wrapped_lines) == 1;

    wide = "";
    for i in range(25) {
        wide = wide + "chunk ";
    }
    set_content(m.state, m.transcript, [wide], 2);
    r2 = compute_layout(m.state, m.screen, Viewport(columns=80, rows=24));
    assert r2.ok;
    e2 = _published(m.state).entries[tid];
    assert len(e2.wrapped_lines) >= 2;
}
