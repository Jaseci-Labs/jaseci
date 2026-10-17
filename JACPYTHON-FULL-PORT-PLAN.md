# JacPython full-port pathway: from the object layer to a Jac evaluator

Companion to `JACPYTHON-OBJECTS-PLAN.md` (which covers the object-port PR in
detail — Mac recipes, guards, `objdump` method). This document is the roadmap
for the rest: every remaining C compilation unit of CPython replaced by
`jac/jaclang/runtime/python/*.jac`, ending with `ceval.c`.

Tracked as jaseci-labs/jac#9994 (epic), #9993 (perf follow-up), PR #9930
(first object layer). Written 2026-10-11 against branch `jacpython-perf`
head `56e9d80658`.

## 0. What "done" means

`JACPYTHON=1 zig build` produces a `python3.14` whose `Makefile.pre.in`
objects list contains no `Python/`, `Objects/`, `Parser/`, or `Modules/` C
unit with a Jac equivalent — the interpreter loop itself runs compiled Jac.
Success is measured by CPython's own suite: the stdlib `test_*` files pass at
the same rate as stock C 3.14.6, and the `jacpython-perf` table shows no
sustained row above ~1.05 vs C.

Not required for "done": `optimizer.c`/tier-2/JIT (may stay C or be
disabled — the build already runs without them), and C-only stdlib modules
nobody has ported (`_ssl`, `_decimal`, `sqlite3` — these can stay C forever;
they're bindings to external libraries anyway).

## 1. The mechanism (same recipe, every layer)

For each C unit:

1. Port the file to `runtime/python/<name>.jac`, implementing the same
   exported symbols and ABI (see the `def:pub` + reserved-symbol rules in
   the objects plan §2 — ports ARE the C definitions).
2. Regenerate `cpython_api.jac` (`gen_capi.jac` keeps declarations for
   cross-port callers — a Jac port still needs the C declaration visible to
   units not yet ported).
3. Drop the `.o` in `bootstrap/python/compiler-bridge.patch` and drop the
   C source from `cpython-sources.txt`.
4. Verify: kernel-off `jac check`, `JACPYTHON=1 zig build` on the Mac under
   the 20 GiB guard, the sanity suite, CPython stdlib tests for that unit,
   push and read `jacpython-perf`.

Ordering matters more than mechanism: porting a unit whose dependencies are
still C buys little (the Jac code calls C for everything real) and risks
re-porting when the dependency changes shape. Port leaves-down.

## 2. Dependency-ordered roadmap

### Phase A — finish the current layer (in flight)

- #9993: call-path perf on the 9 existing ports (fn-pointer calls,
  `alwaysinline` refcounts, wrapping arithmetic).
- Fix the three compiler parity gaps blocking stdlib tests: `+False` and
  `(1,2)*5` constant folding, class-body `LOAD_NAME` vs `LOAD_GLOBAL`.
  These live in the Jac frontend, not the ports.

### Phase B — fundamental objects

Everything below calls these on every operation; until they're Jac, every
existing port pays C-call overhead for its real work.

- `longobject` — `PyLong_*` is the hottest ABI surface in the runtime
  (range/slice/enum ports call it per element). Port has to match C's
  small-int cache and `ob_digit` layout exactly.
- `unicodeobject` — `PyUnicode_*`; CPython's three-kind flexible storage
  (1/2/4-byte) must be reproduced; biggest single-object win after long.
- `dictobject` — `tp_iter`/`lookup`/`PyDict_*` feed everything including
  module namespaces (already-ported `namespaceobject` is built on it).
  Combined-table/split-keys duality is the tricky part.
- `typeobject` — **the keystone, deliberately last in this phase.** `tp_*`
  slots, MRO computation, attribute lookup, `__dict__`/`__slots__`
  descriptors. ~11k lines of C; every other port currently borrows C-side
  type machinery. After this lands, Jac objects own their own dispatch
  end-to-end and several existing residue calls disappear for free.

### Phase C — containers and code objects

- `listobject`, `tupleobject`, `setobject`, `floatobject`, `bytesobject`,
  `bytearrayobject`, `memoryobject`. `list`/`tuple` first (the bench
  controls `ctl_list_*` measure them); `floatobject` is small.
- `funcobject`, `codeobject`, `methodobject`, `classmethodobject`,
  `staticmethod`, `property`, `weakrefobject`, `descrobject`, `genobject`,
  `coroutine`/`asyncgen` objects, `frameobject`. These are the bridge to
  Phase E — `ceval` manipulates code/frame/function objects directly, so
  they must exist in Jac first.
- Remaining `Objects/` leaves: `structseq`, `odictobject`, `tuple`/`list`
  iterators (`iterobject.jac` already provides the machinery pattern),
  `exceptions.c` (technically `Objects/` or `Python/` depending on file —
  port as a unit, `test_exceptions` gates it).

### Phase D — runtime plumbing

- `import.c` + `importdl` — module loading; ties into the already-Jac
  `bindings/module.jac`.
- `pystate` — interpreter/thread state, GIL structures (the
  free-threaded-vs-GIL paths; stick to the GIL build).
- `initconfig`/`preconfig` — interpreter bootstrap; low risk, mostly data
  shuffling, but on the startup critical path.
- `marshal` — needed by `import` for `.pyc`; port with it.
- `exceptions.c`, `codecs` C helpers, remaining `Modules/*.c` worth
  porting (already ~30 done in `bindings/`).

### Phase E — allocator and GC (can interleave with C/D once objects stabilize)

- `obmalloc` (pymalloc) — self-contained but bit-twiddly (arena/pool/usepools
  bitmaps); wrong = silent corruption. Port last among "normal" units; the
  C allocator works fine under Jac objects (they call `PyObject_Malloc`
  today anyway).
- `gc.c` — needs `tp_traverse`/`tp_clear` correct in every ported object
  (already implemented via `jacpy_visit`; #7446 landed the deep-release
  contract for this). `test_gc` is the gate.

### Phase F — the evaluator (last, and it's its own project)

- `ceval.c` — in 3.14 the instruction bodies live in
  `Python/bytecodes.c` and are generated into `generated_cases.c.h`, which
  makes the port *mostly mechanical*: one Jac function per opcode family,
  same stack semantics. The genuinely hard parts:
  - **Threaded dispatch**: computed goto has no Jac equivalent. A switch
    dispatch costs roughly what the dispatch table costs C — acceptable;
    measure on the first working build, not before.
  - **Quickening/specialization** (`specialize.c`, inline caches):
    bytecode self-modifies at runtime — needs `PyCodeObject`/`funcobject`
    (Phase C) and a Jac-side adaptive path, or ship non-adaptive first
    (`--disable` equivalent: leave `specialize.c` C while `ceval` is Jac).
  - **Inline caches / `PyStackRef`** tagging in 3.14's eval loop.
- `optimizer.c`, tier-2, JIT: leave C or disable. Not needed for "done".

## 3. Hard walls (known before starting)

- `typeobject`: largest `.c` in Objects; touches every ABI invariant the
  other ports assume. Budget an entire PR for it; sequence it when the
  fundamentals are stable so its callers are already Jac.
- `ceval` dispatch: no computed goto → switch; quantify on a real build
  before optimizing speculatively.
- `obmalloc`: silent-corruption failure mode; needs its own stress harness
  (`test_bigmem`/`regrtest -R` refleak runs) not just the sanity suite.
- GC `tp_traverse` subtlety: already bitten once (#7446); add a
  traverse-coverage check to the port checklist.
- ThinLTO: zig 0.16 clang is LLVM 21 vs Jac's LLVM 22, so C helpers can't
  inline into `jacpython.o`. If the toolchain aligns later, freelist/GC
  helper calls collapse — rebench then.
- `itertools.repeat` Jac binding is ~20×/iter slower than C and adds a
  flat +45 ns tax to anything under `timeit` — fix it before trusting
  fine-grained benches (own issue/PR).

## 4. Working rules (carried over — each cost hours)

1. Ports are C definitions: `def:pub` keeps the bare symbol under
   `runtime/python/`; everything else is renamed by the reserved-symbol
   machinery. Never reach around the rename.
2. `compiler-bridge.patch` hunks are zero-context against **pristine**
   Python 3.14.6 `Makefile.pre.in` — verify with `patch -F0 --dry-run`
   and renumber `+new` lines of later hunks when adding a removal.
3. Every perf change: kernel-off `jac check` → native object build →
   disassemble (`objdump -dr`, count `bl`/`b.vs`) → push → read CI table.
   Never reason about hot paths without the disassembly.
4. Mac builds under the 20 GiB process-tree guard (`/tmp/tguard.py` —
   `start_new_session=True` so the kill group excludes the guard itself;
   the earlier bash version killed its own pgid).
5. `jacpy_*` helpers are the residue surface: `grep -n "jacpy_[a-z_]*("
   runtime/python/*object*.jac | grep -v "def jacpy_"`, classify hot/cold,
   only hot ones justify a helper.

## 5. Progress log

- 2026-10-11 — Object layer merged-pending (PR #9930, all CI green);
  perf parity confirmed; epic #9994 + follow-up #9993 filed; this
  pathway written. Next work item per §2: Phase A items, then
  `longobject`.
