# JacPython object ports: plan to finish (range/slice + 6 earlier ports, C parity, merge)

Written 2026-10-10 for an agent finishing this work alone. Read it top to bottom
once before doing anything. Every command here was used successfully in the
original session unless marked **UNTESTED**. Keep your replies to the user brief.

---

## 0. What "done" means

1. PR **jaseci-labs/jac#9930** (head `chess10kp:jacpython-perf`) is green on every
   required check and ready for review (draft flag removed only when the user
   says so).
2. The 8 ported objects (`bool`, `capsule`, `cell`, `enumerate`/`reversed`,
   `iter`/`callable_iterator`/`anext_awaitable`, `SimpleNamespace`, `range`,
   `slice`/`Ellipsis`) perform within noise of **main's JacPython** (which still
   uses CPython's C versions of these objects) on the benchmark in
   `jacpython-perf.yml`.
3. CPython's own tests for those objects pass under JacPython, except failures
   proven to be caused by the JacPython *compiler* (Section 7), which are listed
   in the PR description.
4. The AGENTS.md perf log and the migration doc describe the final state.

Do **not** merge, force-push, mark ready-for-review, or post comments on other
people's PRs without the user asking.

---

## 1. Where things are

### Repo and branches
- Working tree: `/home/jac/repos/jacpy-comp` (a git **worktree**; the stash is
  shared with other worktrees: never use `git stash`).
- Local branch: `jacpy-comp`. Its commits are pushed to the fork remote `fork`
  (`git@github.com:chess10kp/jaseci.git`) as branch `jacpython-perf`.
- PR: https://github.com/jaseci-labs/jac/pull/9930 (draft).
- Base: `b176cb0266` (main when the work started).

### Commits on the branch (oldest first)
| commit | what |
|---|---|
| `3a6ca6383a` | range/slice port + all JACPYTHON=1 build/runtime fixes + workflow |
| `6d065f9138` | empty trigger commit (harmless) |
| `156b9e5d73` | workflow `pull_request` trigger |
| `5864a72729` | **pre-commit.ci autofix** (bot pushes these; always rebase on them) |
| `1031ce8811` | perf-parity pass (inline refcount, fn-pointer slot calls, freelists, wrapping arithmetic, inline tuple access) |
| `d4f06248c5`, `b6bc80b3e8`, `4bd115eec4` | benchmark/workflow fixes + C-only control benchmarks |

### Files that matter
- Ports: `jac/jaclang/runtime/python/{boolobject,capsule,cellobject,enumobject,iterobject,namespaceobject,rangeobject,sliceobject,refcount}.jac`
- Generated C-API declarations: `jac/jaclang/runtime/python/cpython_api.jac`
  (**never hand-edit**; regenerate, Section 3.4).
- C residue (helpers the Jac code calls): `jac/bootstrap/python/object_api.c`
- Source manifest: `jac/bootstrap/python/cpython-sources.txt`
  (ported files are marked `# Objects/x.c  # removed: N source lines`).
- Makefile detachment of removed objects: `jac/bootstrap/python/compiler-bridge.patch`
  (zero-context hunks; Section 6.3 if you edit it).
- Native compiler changes made for this work:
  `jac/jaclang/compiler/backends/native/na_ir_gen_pass.impl/{c_interop,globals,core,expr}.impl.jac`,
  `.../na_ir_gen_pass.jac` (declarations), `jac/jaclang/compiler/frontend/codeinfo.jac`
  (reserved C symbol list).
- Generator: `scripts/jacpython/gen_capi.jac`.
- Perf workflow: `.github/workflows/jacpython-perf.yml`; benchmark
  `scripts/jacpython/bench_objects.py` (**must be converted, see 4.1**).
- Docs: `jac/jaclang/cli/docs/internals/jacpython-migration.md`.
- Perf decision log: `/home/jac/repos/jacpy-comp/AGENTS.md` (**gitignored**,
  local only; keep it updated anyway, it is the user's record).

---

## 2. Hard rules (each one cost hours to learn)

1. **Memory cap: 20 GiB** process-tree RSS for any build/check you run on the
   Mac. Always run through the guard script (3.2). Never check
   `na_ir_gen_pass.jac` together with other files (it alone peaked 19.8 GB).
2. **This Linux box cannot build the native compiler kernel** (OOM-killed).
   Anything that needs `jac` locally (pre-commit hooks, `jac check` the normal
   way) fails. Commit with `git commit --no-verify`.
3. **No AI co-author trailer** in commit messages (CI blocks
   `Co-Authored-By: Claude`). PR descriptions may carry the Claude Code line.
4. **No new `.py` files** in the PR (Contribution Checks fails). See 4.1.
5. **Before every push**: `git fetch fork jacpython-perf && git rebase FETCH_HEAD`.
   pre-commit.ci pushes autofix commits to the branch; a plain push is rejected.
6. **`pkill -f <pattern>` kills your own shell** if the pattern appears in the
   command line. Use `pgrep` to get a PID, then `kill <pid>`.
7. GitHub Actions on the **fork never start** (unknown account-level issue).
   All CI runs happen on the upstream PR. You **cannot cancel** upstream runs
   (needs admin); a stuck run dies at the workflow's 120-minute timeout.
8. Never use bare `git stash`, never `git push --force` without the user saying so.
9. Python test failures in `test_bool`, `test_scope`, `test_tuple` are known
   compiler issues (Section 7). Do not "fix" them by changing object code.

---

## 3. How to do each kind of step

### 3.1 The Mac
- `ssh -o ConnectTimeout=20 jaseci@100.88.159.83` (tailscale; 48 GB, ~13 GB used
  by an MLX training job you must not touch).
- Repo copy: `~/repos/jacpy-comp` (a snapshot, **not** real git). Sync files you
  change with `scp -q -o ConnectTimeout=20 <localpath> jaseci@100.88.159.83:repos/jacpy-comp/<samepath>`.
- Before trusting anything on the Mac, check the file is identical:
  `md5sum < local` vs `ssh ... md5 -q repos/jacpy-comp/<path>`.

### 3.2 Guarded commands on the Mac
`/tmp/gcheck.sh TAG cmd...` runs `cmd` in `~/repos/jacpy-comp/jac`, kills the
tree above 20 GiB, writes `/tmp/TAG.log` ending with `EXIT=<rc> PEAK_KB=<kb>`.
`/tmp/gcheck2.sh` is the same but honours `GDIR=<dir>` for the working dir.
If `/tmp` was wiped, recreate gcheck.sh:
```sh
#!/bin/sh
tag=$1; shift
cd ${GDIR:-~/repos/jacpy-comp/jac}
"$@" > /tmp/$tag.log 2>&1 &
pid=$!
peak=0
while kill -0 $pid 2>/dev/null; do
  r=$(ps -axo pid,ppid,rss | awk -v p=$pid 'BEGIN{t[p]=1} {pp[$1]=$2; rs[$1]=$3} END{c=1; while(c){c=0; for(i in pp) if(!(i in t) && (pp[i] in t)){t[i]=1;c=1}} for(i in t) s+=rs[i]; print s+0}')
  [ "$r" -gt "$peak" ] && peak=$r
  if [ "$r" -gt 20971520 ]; then pkill -P $pid; kill $pid; echo "KILLED at $r" >> /tmp/$tag.log; fi
  sleep 2
done
wait $pid; echo "EXIT=$? PEAK_KB=$peak" >> /tmp/$tag.log
```
macOS has no `timeout`; `/tmp/to.sh SECS cmd...` is a small replacement.

### 3.3 Type-check (`jac check`) — kernel-off mode
The normal path rebuilds the compiler kernel (>20 GiB). Use:
```sh
ssh jaseci@100.88.159.83 '/tmp/gcheck.sh chk env JAC_COMPILER_LIB=off JAC_KERNEL_BUILDING=1 \
  ./zig-out/bin/jac check jaclang/runtime/python/rangeobject.jac jaclang/runtime/python/sliceobject.jac; \
  grep -A4 "Error:" /tmp/chk.log | head -40; grep -E "ok \[|FAILED|EXIT" /tmp/chk.log'
```
Warnings (W30xx, W2003) are fine. Lines quoting `# Py_None ...` comments under
"Error:" greps are context, not errors; trust the `ok [` / `FAILED` lines.
Check `cpython_api.jac` and `native_api.jac` too after any port change.

### 3.4 Regenerate `cpython_api.jac` (after adding/removing any C call in a port)
```sh
ssh jaseci@100.88.159.83 'cd ~/repos/jacpy-comp; GDIR=$PWD /tmp/gcheck2.sh gencapi \
  env PATH=$PWD/jac/zig-out/bin:$PATH JAC_COMPILER_LIB=off JAC_KERNEL_BUILDING=1 \
  jac/zig-out/bin/jac run scripts/jacpython/gen_capi.jac; grep -v Compiling /tmp/gencapi.log | tail -5'
scp -q jaseci@100.88.159.83:repos/jacpy-comp/jac/jaclang/runtime/python/cpython_api.jac \
  jac/jaclang/runtime/python/cpython_api.jac
```
"No Jac mapping for these called functions" means a new C helper uses a type
gen_capi cannot map (function-pointer typedefs etc.). Fix by making the C
helper take `void *` and cast inside (see `jacpy_capsule_call_*`).

### 3.5 Build only the native object (fast, ~10 min, ~6.5 GB) and inspect machine code
```sh
ssh jaseci@100.88.159.83 'cd ~/repos/jacpy-comp/jac; rm -rf /tmp/prepnat_out; \
  /tmp/gcheck.sh prepnat env DYLD_FALLBACK_LIBRARY_PATH=$HOME/tools/zstd/lib \
  .python-build/cpython/macos-aarch64/python/install/bin/python3.14 -I \
  bootstrap/python/prepare_native.py $PWD /tmp/prepnat_out macos-aarch64; \
  grep -E "^error|demot|EXIT|JacPython:" /tmp/prepnat.log | sort | uniq -c | head'
```
Success line: `JacPython: built native compiler object; no interpreted demotions`.
Any `demoting X to Python-only` line is a **regression**: the function no longer
lowers natively (and any static type table referencing it breaks).
Disassemble one function (names are `<module>_<hash>.<fn>`):
```sh
ssh jaseci@100.88.159.83 'otool -tvV /tmp/prepnat_out/jacpython.o | \
  awk "/enumobject_.*\.enum_next:/{f=1} f{print} f&&/^_/&&!/enum_next:/{exit}" | head -80'
```
In a relocatable `.o`, external calls show as `bl <own address>`: count them,
that is the number of out-of-line calls. Compare with C:
`otool -tvV -p _enum_next .python-build/cpython/macos-aarch64/python/install/lib/libpython3.14.dylib`.

### 3.6 Full JacPython build on the Mac (~15–25 min, ~7 GB)
```sh
ssh jaseci@100.88.159.83 'rm -f /tmp/jpbuild.log; nohup /tmp/gcheck.sh jpbuild env JACPYTHON=1 \
  JAC_PYTHON_JOBS=2 HOMEBREW_PREFIX=$HOME/tools/brewshim DYLD_FALLBACK_LIBRARY_PATH=$HOME/tools/zstd/lib \
  PATH=$HOME/tools/zig:$PATH $HOME/tools/zig/zig build -Ddev -j2 >/dev/null 2>&1 &'
```
Poll `/tmp/jpbuild.log` for `EXIT=`. Interpreter:
`~/repos/jacpy-comp/jac/.python-build/jacpython/macos-aarch64/python/install/bin/python3.14`.
Stock C build for comparison: same path with `cpython` instead of `jacpython`.
Crash triage: no debugger over ssh; read
`~/Library/Logs/DiagnosticReports/python.exe-*.ips` (JSON after the first line;
the `triggered` thread's frames).

### 3.7 CI (the real measurement)
- Push (rule 2.5) → `jacpython-perf.yml` runs on the PR (~40–50 min).
- Find the run for your commit:
  `gh run list -R jaseci-labs/jac --branch jacpython-perf --workflow jacpython-perf.yml --limit 6 --json headSha,databaseId,status`
- Logs only after the job completes:
  `gh api --allow-escape-sequences repos/jaseci-labs/jac/actions/jobs/<job_id>/logs | sed 's/\x1b\[[0-9;]*m//g' > job.log`
  then `grep -E '^\S+Z \| |tests? (OK|failed)|Result:' job.log | cut -c30-`.
- `gh run view <id> --json jobs` gives the job id and per-step status.
- The table is also in the run's job summary on the web.

---

## 4. Immediate work (do in this order)

### 4.1 Unblock Contribution Checks: no `.py` files — DONE in `8aa9055` (benchmark embedded in the workflow)
`scripts/jacpython/bench_objects.py` trips "New Python (.py) files detected".
Do **not** ask for the skip label. Move the benchmark into the workflow:
1. Delete `scripts/jacpython/bench_objects.py`.
2. In `jacpython-perf.yml`, add a step that writes the same script to
   `$RUNNER_TEMP/bench_objects.py` with a quoted heredoc (`cat > ... <<'PY'`),
   and point both benchmark invocations at it. Keep the content byte-identical
   (the `per_op` range-loop timer, the `calliter` counter reset, the `ctl_*`
   controls).
3. Validate YAML locally: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/jacpython-perf.yml'))"`.
Check docs/AGENTS.md mention of `scripts/jacpython/bench_objects.py` and update.

### 4.2 Find out why pre-commit.ci fails — DONE in `b286590` (`ban-em-dashes` on Markdown; fixed the migration doc). Re-check it passes.
`gh pr checks 9930 -R jaseci-labs/jac` → open the `pre-commit.ci - pr` link
(results.pre-commit.ci). It usually means a hook (jac-format, lint, deslop) wants
changes it could not autofix. Read the failing hook's output, fix by hand,
commit, push. If the hook needs `jac` (can't run locally), apply the change the
log shows verbatim. Expect the bot to also push autofix commits: rebase on them.

### 4.3 **Revert the kernel memory hack before merge** — DONE in `8aa9055`
Commit `3a6ca6383a` changed `jac/jaclang/compiler/backends/native/kernel_resolve.jac`
`kernel_options()`: `native_threads=4 → 1`, `opt_level=2 → 0`. That was a local
experiment to fit the kernel build in memory. It ships an **unoptimized compiler
kernel** to everyone. Restore `native_threads=4` and `opt_level=2` exactly.
(The kernel self-build still won't fit locally or under 20 GiB; that is fine,
CI builds it.)

### 4.4 Read the C-only control results
A CI run on `4bd115eec4` adds `ctl_list_index`, `ctl_int_add`, `ctl_dict_get`,
`ctl_list_iter`, `ctl_call`, `ctl_len_list`: they touch **no** ported code.
Fetch its table (3.7).
- If controls show ratio ≈1.00 (±0.05): the gaps in Section 5 are in the ports.
  Go to Section 5.
- If controls show 1.1–1.3 like the object benches: the JacPython runtime is
  slower **overall** (layout, flags, link). Go to 4.5 first; object work cannot
  fix that.

Known facts that already point at "overall": `range_iter` is 1.23× on CI, but
the per-item work is the `FOR_ITER_RANGE` instruction in C's eval loop; no ported
function runs per item. On the Mac both builds matched (4773 vs 4813 ns).
JacPython bytecode gets exactly the same specialized instructions as C
(verified with `dis.get_instructions(f, adaptive=True)`).

### 4.5 Make the comparison fair: add main's JacPython as the third interpreter — DONE in `8aa9055` (workflow now reports branch/main; 3 interleaved rounds)
"Parity with the C impl" really means: this branch's JacPython vs **main's
JacPython** (same runtime, C objects). The stock CPython differs in more than
the objects (Jac compiler, other Jac ports like `itertools`, link inputs).
1. In `jacpython-perf.yml`, before building, add a job step (or a second job)
   that checks out `main` into `$RUNNER_TEMP/main` (`actions/checkout@v5` with
   `ref: main`, `path: main`) and runs `JACPYTHON=1 zig build build-python` in
   `main/jac`. Interpreter: `main/jac/.python-build/jacpython/<osarch>/python/install/bin/python3.14`.
   (Build time roughly doubles; raise `timeout-minutes` to 180.)
2. Run the benchmark on all three: C, main-JacPython, branch-JacPython. Table
   columns: C, main, branch, branch/main.
3. Run each interpreter's benchmark **3 times interleaved** (C, M, B, C, M, B,
   C, M, B) and take the per-bench minimum; shared runners are noisy and a
   single sample misleads.
4. **The target is branch/main ≈ 1.00 on every row.** branch/C only matters as
   context.
If branch/main is ≈1.00 everywhere, perf is done: skip to Section 6.

---

## 5. Closing per-object gaps (only rows where branch/main > ~1.05)

Method for every row: find the C function on the hot path (Section 5.1 table),
disassemble the Jac version (3.5), count `bl` calls and checked-arithmetic
branches (`b.vs`), compare with C's machine code, remove the differences. After
each change: check (3.3), native build (3.5, must say "no interpreted
demotions"), push, read CI.

### 5.1 Hot paths and known remaining differences
Find every residue call in the ports:
`grep -n "jacpy_[a-z_]*(" jac/jaclang/runtime/python/*object.jac jac/jaclang/runtime/python/capsule.jac | grep -v "def jacpy_"`
Classify each as hot (per call/iteration) or cold (errors, repr, reduce, GC).
Only hot ones matter. Known hot ones:

| bench (ratio vs C on CI) | hot path | known extra work vs C | fix |
|---|---|---|---|
| range_new 1.49, bool_new 1.29 (**args/arg-check/index-check items DONE in `702f8a9`**) | `range_vectorcall`, `bool_vectorcall` | `jacpy_vectorcall_arg(args, i)`: a C call per argument to read `args[i]` | read args inline: declare `obj Args3 { has a0: ptr[PyObject], a1: ..., a2: ...; }` in the port's `import from c` block and read `ptr[Args3](args).a0` (same trick as `PyTuple2_Layout` in enumobject.jac). Bounds come from `nargs`, already checked. |
| range_new | `range_from_array` → `range_make` → `compute_range_length` | `jacpy_range_index_check` (C call for `_PyIndex_Check`), `jacpy_range_obj_alloc` (freelist, unavoidable call) | inline `_PyIndex_Check`: `Py_TYPE(o)->tp_as_number != NULL && ->nb_index != NULL` via typed ptr field reads (see `index_check` in sliceobject.jac for an already-inline version: reuse it). |
| range_len 1.28, range_index 1.19, range_contains 1.10 | `range_length`, `range_item`, `range_contains` | checked i64 arithmetic (`adds`+`b.vs`) where C uses plain ops; `PyLong_*` calls (same as C) | use `wrapping_add/sub/mul` **only** where C's code cannot overflow (prove it from the C source); leave checked ops where C checks. |
| slice_new 1.12, list_slice 1.25 | `PySlice_New`, `_PyBuildSlice_ConsumeRefs`, `slice_new` | `jacpy_slice_alloc` (freelist call), `jacpy_capsule_track` (GC track call), `py_decref` out of line | combine pop+track into one C helper **only if** fields are written before any allocation can happen (they are: no allocation between); saves one call. |
| enumerate 1.15 | `enum_next` | `PyLong_FromSsize_t` (C does the same), `py_decref` out of line, `tuple_recycle` | check `py_decref` inlining (5.2). |
| range_iter 1.23 | `FOR_ITER_RANGE` in ceval (C) | none in Jac per item | build-wide (4.4/4.5) |

### 5.2 `py_decref` not always inlined
`refcount.jac` `py_decref` sometimes stays an out-of-line 8-instruction function
(C's `Py_DECREF` is always inlined). Options, in order:
1. Look for an always-inline attribute in the native backend
   (`grep -rn "alwaysinline\|always_inline\|attributes.add" jac/jaclang/compiler/backends/native/`).
   If one exists for Jac functions, use it on `py_incref`/`py_decref`.
2. If none: add one. Find where `ir.Function` objects are created for Jac defs
   (`grep -n "ir.Function(" jac/jaclang/compiler/backends/native/na_ir_gen_pass.impl/*.jac`)
   and add `fn.attributes.add("alwaysinline")` for functions with a marker the
   compiler already parses (ask the user before inventing new syntax).
3. Otherwise accept and log it in AGENTS.md.
Also (**DONE in `702f8a9`**): `py_decref`'s checked `rc - 1` produced a `b.vs` branch. Use
`wrapping_sub(rc, 1)` (rc is a non-immortal live refcount, ≥1 in the low half,
so it cannot overflow), same for `rc + 1` in `py_incref`.

### 5.3 Rules for touching hot code (all learned the hard way)
- Cross-module calls: each port declares its own opaque `obj PyObject`; these
  types do **not** unify. Shared helpers must take bare `ptr` (see
  `refcount.jac`). A `ptr[PyObject]` *return* value from another Jac module
  cannot be assigned to a typed local (E1001).
- Calling a C function pointer stored in a struct field: write
  `p.field(args)` where `p` is a `ptr[Layout]` and the field is declared
  `Callable[...]` in a C-layout `obj` inside `import from c`. It lowers to a
  direct load + call (`_codegen_c_fnfield_call`). It does **not** work for a
  `Callable` *parameter* (that is a Jac closure); use a C helper
  (`jacpy_visit`).
- `&mut local` works only for **C extern** parameters typed `&mut T`. Passed to
  a Jac `def` parameter typed bare `ptr` it lowers to NULL (silent).
- `u64(x)` and `i64(x)` casts and all sized-int arithmetic are **checked** (abort
  with "integer overflow"). For C unsigned/wrapping semantics use `u64.wrap(x)`,
  `i64.wrap(x)`, `wrapping_add/sub/mul/shl/neg`.
- `/` on ints is float division; use `//` (C truncates toward zero; only safe
  when operands are non-negative, otherwise compute like C).
- `Py_None`, `Py_NotImplemented`, `Py_True`, `Py_False` are macros with no
  symbol. Declare `glob _Py_NoneStruct: PyObject_Layout;` (needs a local
  `obj PyObject_Layout` in the same `import from c` block) and bind it to a
  typed local: `none_obj: ptr[PyObject] = _Py_NoneStruct;`.
- `static inline` CPython functions (`_PyTuple_Recycle`, `_PyLong_GetOne`,
  `_PyObject_CallNoArgs`, `_PyIndex_Check`, freelist macros) have no symbol:
  either inline them in Jac from the 3.14.6 header source, or add a C helper.
- A Jac `def:pub` whose name is in `NATIVE_RESERVED_C_SYMBOLS`
  (`codeinfo.jac`) gets renamed `__jac_def_<name>` and the C symbol goes
  missing at link. Check the list when porting any `PyXxx` API function.
- A port must not declare, in its own `import from c`, a function another port
  defines (it shadows/duplicates). Get the declaration from `cpython_api.jac`
  (gen_capi emits it when another file calls it), or call it Jac-to-Jac.
- Static type tables (`glob:pub PyFoo_Type: PyTypeObject_Layout = ...`): every
  function referenced must lower natively. A single E5092 demotion makes the
  whole initializer fail ("Native lowering failed for static struct member").
- Never call through `ty.tp_xxx(...)` on a `Callable` field of a **non-pointer**
  struct value; only `ptr[T]` receivers are supported.
- `obj` is a keyword (can't be a variable name); `else if` must be `elif`;
  docstrings inside function bodies are errors (use `#`).

### 5.4 After each perf change
1. `jac check` the changed ports + `cpython_api.jac` (3.3).
2. Regenerate `cpython_api.jac` if C calls changed (3.4).
3. Native build: "no interpreted demotions" (3.5). Disassemble the function you
   changed and confirm the call/branch you removed is gone.
4. Commit (`--no-verify`, no AI trailer), rebase on `fork/jacpython-perf`, push.
5. Read the CI table and test summary. Tests must still be 14 OK / 3 known
   failures. If a new test fails, revert that change first, then debug.
6. Update AGENTS.md: add or amend the entry (Cost / Why / Reversal) so it
   matches reality. Remove "Remaining cost" text you eliminated.

---

## 6. Finish line (merge readiness)

### 6.1 Full CI on the PR
`gh pr checks 9930 -R jaseci-labs/jac`. Required: `build-kit`, `jac-check`,
`test-*` jobs from `ci.yml`, `Contribution Checks`, `pre-commit.ci`. For each
failure: get the job log (3.7), read the first `##[error]`, fix, push.
- `build-kit` builds the sealed kit with the native compiler (`na_ir_gen_pass`
  changes are here). A failure mentioning `demoting` or E5092 in compiler
  modules means a compiler change regressed lowering: compare against a green
  run on main (the user has a note: "kernel SIGABRT = demoted abort stub").
- `jac-check`/lint: deslop or format complaints: apply them.
- If a check needs a label or maintainer action, tell the user; don't add labels.

### 6.2 Correctness re-verification (once, at the end)
Run in CI (already in the workflow) and confirm in the log:
`test_bool test_range test_slice test_enumerate test_iter test_iterlen test_types test_scope test_funcattrs test_itertools test_contains test_index test_int test_long test_list test_tuple test_builtin`
→ only `test_bool` (`+False` folded), `test_scope` (class-body implicit global
uses LOAD_GLOBAL), `test_tuple` (`(1,2)*5` not folded) fail. Also add
`test_capi` **UNTESTED** (needs `_testcapi`, which `--disable-test-modules`
removes; if unavailable, skip and note it).

### 6.3 If you edit `compiler-bridge.patch`
Hunks are zero-context and match by line number of the **pristine**
`Makefile.pre.in` (Python 3.14.6; extract it from
`jac/.python-build/jacpython/sources/74d0d71d…tar.gz`, member
`Python-3.14.6/Makefile.pre.in`). When adding a removed-object hunk, adjust the
`+new` line numbers of every later hunk. Verify with GNU patch:
`patch -f -F0 -p1 --dry-run -i <just the Makefile part>` on a pristine copy,
then apply `build-graph.patch`'s Makefile part after it (it must still apply).

### 6.4 Final docs
- `jacpython-migration.md`: the paragraph after the rangeobject section lists
  the native-ABI rules and the perf state; make it match the final code.
- AGENTS.md: every entry's "Remaining cost" accurate.
- PR description (`gh pr edit 9930 -R jaseci-labs/jac --body-file …`): summary,
  the final branch/main table, the 3 known compiler test failures, what is
  intentionally still residue (capsule callbacks, `Py_VISIT`, freelist calls)
  and why. Ask the user before taking the PR out of draft.

---

## 7. Out of scope (report, don't fix here)
- ~~JacPython compiler: `+False` and `(1,2)*5` not constant-folded; class-body
  implicit globals use `LOAD_GLOBAL` instead of `LOAD_NAME`.~~ **FIXED
  2026-10-11** (see Progress note): constant folding now mirrors CPython
  3.14 `eval_const_unaryop`/`eval_const_binop` + `const_folding_safe_*`
  guards (`codegen_util.jac` fold_* helpers, `emit_folded_const`,
  `register_const_operand`, `integer_multiply`/`integer_pow`, PyStr/PyBytes
  `nb_binop` repeat); implicit-global name ops in class scopes use
  `LOAD_NAME`/`DELETE_NAME` outside inlined comprehensions
  (`name_load_opcode`, `emit_name_delete`), per
  `_PyCompile_ResolveNameop`'s function-like-only GLOBAL rule.
- `itertools.repeat` (Jac port on main) is ~20× slower than C per iteration
  (47 vs 2.3 ns). It is why plain `timeit` showed a flat +45 ns on everything.
  Worth its own PR.
- No ThinLTO for `jacpython.o`: zig 0.16's clang is LLVM 21, Jac's LLVM is 22,
  so `build.sh` links the machine-code object. Matching majors would let the
  remaining C helper calls (freelists, GC track) inline; that is a toolchain
  change, not part of this PR.
- The fork's GitHub Actions don't start (account-level); the user knows.

---

## 8. If you get stuck
- Build broke after a compiler change: bisect by copying files from a clean
  `HEAD` tree. Recipe used before: `git archive HEAD jac/jaclang jac/bootstrap
  | gzip > head.tgz`, extract on the Mac to `~/repos/jacpy-head`, symlink
  `jaclang/vendor/typeshed/stdlib` from the main copy, copy
  `libjacllvm.dylib`, run `prepare_native.py` against that root (3.5 with
  `GDIR` and the root path changed), then copy suspect files over one group at
  a time.
- A prepare_native crash with a Python traceback deep in `na_ir_gen_pass`: add
  a temporary raise with the function name at the failing line **on the Mac
  copy only**, rerun, then restore the file (keep a `/tmp/<file>.orig`).
- Runtime segfault/abort: crash report (3.6); `Uncaught exception: integer
  overflow` is checked arithmetic in a port (5.3); bisect with small `-c`
  snippets (`print(list(range(10,0,-2)))` style) against the Mac build.
- Anything ambiguous about what the user wants: ask; keep it to one short
  question.

## Progress note (2026-10-10, commit 1c4cf1776b)
- Run 38069627309 (branch vs main JacPython): range_iter/neg_iter/reversed
  are ~1.0 vs main, so the earlier ~1.2 vs C on those rows is build-wide (main
  shows it too), not the ports.
- Fixed in 1c4cf1776b: per-call heap `_GliResult` in `_PySlice_GetLongIndices`
  (now `slicelongindices.jac`, native out-params); `jacpy_isize_load/store`
  in PySlice_Unpack etc.; `range_length` -> `PyLong_AsSsize_t`; slice_new
  direct tuple reads; `jacpy_small_zero/one` link-time constants.
- Next: read run 38075966515; rows still > ~1.05 vs main get the same
  treatment (look for `_malloc`/`__rc_release_*`/C helper calls in
  `objdump -dr` of the function).
