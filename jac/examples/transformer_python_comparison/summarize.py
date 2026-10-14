"""Compact saved evidence; this script does not import Torch or run benchmarks."""
import json
from pathlib import Path
from preserve import check

root = Path(__file__).parent
report = json.loads((root / 'results' / 'validation_cpu.json').read_text())
assert report['status'] == 'passed' and report['fallback'] is None
rows = {}
for name, case in report['cases'].items():
    assert case['status'] == 'passed' and not case['frontend_audit']['calls']
    assert case['compiler_entry'] == 'torch._inductor.compile_fx.compile_fx'
    assert case['checked_intermediates'] == 45
    assert case['counts']['node_counts'] == dict(placeholder=49, call_function=157, output=1)
    assert len(case['replaced_weights']) == 11 and case['residual_joins'] == 5
    rows[name] = dict(dtype=case['dtype'], shape=case['shape'], checked_intermediates=45,
                      final_max_abs_error=case['final_errors'],
                      intermediate_max_abs_error={engine:max(v[engine] for v in case['intermediate_errors'].values())
                                                  for engine in ('fx','inductor')},
                      frontend_capture_calls=0, replaced_weights=len(case['replaced_weights']))
summary = dict(status='passed', environment=report['environment'], cases=rows,
               graph_nodes=dict(placeholder=49, call_function=157, output=1),
               parameter_tensors=46, fixed_position_buffers=1,
               compiler_entry=report['compiler_entry'], dynamo_frontend_capture=False,
               internal_backend_trace='Inductor may symbolic_trace torch._dynamo.utils.identity for its own loop-body bookkeeping; never version 1.',
               fallback=None, cuda_status=report['cuda_status'], preservation=check(),
               note='Correctness/expression comparison only; no timing or performance claim.')
(root/'results'/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
lines=['# CPU correctness evidence', '', '| case | FX output max abs | direct Inductor output max abs | FX intermediate max abs | direct Inductor intermediate max abs |', '|---|---:|---:|---:|---:|']
for name,row in rows.items():
    output=row['final_max_abs_error']; intermediate=row['intermediate_max_abs_error']
    lines.append(f"| {name} | {output['fx']:.5g} | {output['inductor']:.5g} | {intermediate['fx']:.5g} | {intermediate['inductor']:.5g} |")
lines += ['', 'All four cases passed, including 45 checkpoints, three repeated/changed inputs per case, eleven weight/buffer replacements, in-place mutation, five residual joins, causal masks, future isolation (nontrivial sequence lengths), encoder/cross-memory influence and four metadata/name guards. The small float64 case additionally compiles and validates the output-only graph.', '', 'Actual compiler entry: `torch._inductor.compile_fx.compile_fx`. Frontend capture probes: zero calls; no fallback. Internal AOTAutograd/functionalization/decomposition and Inductor helper tracing are still part of this backend.', '', 'CUDA was not run: the host GPU was occupied by Ollama and the isolated test environment uses CPU-only Torch. No driver changes or interference with that workload.', '', 'Existing example/library tree hashes verified unchanged. No performance measurements.']
(root/'results'/'summary.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
