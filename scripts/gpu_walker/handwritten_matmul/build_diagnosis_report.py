#!/usr/bin/env python3
"""Publish three primary datasets from one interleaved Nsight run plus ablations."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('validation', type=Path)
    args = parser.parse_args()
    root = args.validation
    base = root / 'codegen'
    profile = read(base / 'paired-profile/results.json')
    verified = read(base / 'paired-profile/verified-kernels.json')
    ordinary = read(base / 'paired-ordinary/results.json')
    ablation = read(base / 'ablation-profile/verified-kernels.json')
    ablation_results = read(base / 'ablation-profile/results.json')
    ablation_ordinary = read(base / 'ablation-ordinary/results.json')
    status = read(base / 'status-validation.json')
    codegen = read(base / 'codegen.json')
    for run in ('paired-profile', 'ablation-profile'):
        check = read(base / run / 'verified-kernels.json')
        assert check['status'] == 'PASS'
        assert check['results_sha256'] == sha(base / run / 'results.json')
        assert check['sqlite_sha256'] == sha(base / run / 'trace.sqlite')
    assert status['status'] == 'PASS' and status['gpu_launches_checked'] == 39
    for source in (profile, ordinary, ablation_results, ablation_ordinary):
        assert source['complete']
        assert source['input_sha256'] == sha(root / 'inputs/inputs.json')
        assert all(case['all_outputs_and_statuses_verified'] for case in source['cases'])
        for label, info in source['jac_variants'].items():
            assert info['sha256'] == codegen['transformations'][label or 'baseline']['ptx_sha256']
    # Frozen original sources or the current equivalent replay sources are valid.
    assert profile['runner_sha256'] in (sha(base / 'paired-benchmark.py'), sha(Path(__file__).parent / 'benchmark.py'))
    assert verified['verifier_sha256'] in (sha(base / 'paired-analyze_profile.py'), sha(Path(__file__).parent / 'analyze_profile.py'))
    assert ablation_results['runner_sha256'] == sha(Path(__file__).parent / 'benchmark.py')
    assert ablation['verifier_sha256'] == sha(Path(__file__).parent / 'analyze_profile.py')
    for label, info in codegen['transformations'].items():
        assert info['ptx_sha256'] == sha(base / (label + '.ptx'))
    assert status['ptx_sha256'] == {label: sha(base / (label+'.ptx')) for label in ('baseline', 'O2', 'hoist_sroa')}
    assert status['validator_sha256'] == sha(Path(__file__).parent / 'validate_codegen.py')
    assert codegen['generator_sha256'] == sha(Path(__file__).parent / 'diagnose_codegen.py')

    primary = root / 'primary'
    primary.mkdir(exist_ok=True)
    sources = {key: {'path': 'codegen/' + key, 'sha256': sha(base / key)} for key in (
        'paired-profile/results.json', 'paired-profile/verified-kernels.json',
        'paired-profile/trace.sqlite', 'paired-profile/trace.nsys-rep', 'paired-ordinary/results.json')}
    groups = [('jac_original', 'Jac Predicted', 'Jac: existing production backend and target-machine code generation'),
              ('jac_optimized', 'Jac O2 Predicted', 'Jac: same raw LLVM module plus standard LLVM O2 middle-end'),
              ('handwritten', 'CUDA tiled', 'Handwritten CUDA: fixed 16x16 shared-memory tiled int64 kernel')]
    summaries = {(x['case'], x['arm']): x for x in verified['summaries']}
    ordinary_cases = {x['id']: x for x in ordinary['cases']}
    comparisons = []
    datasets = {}
    for key, arm, description in groups:
        data = {'group': key, 'description': description, 'arm': arm,
                'unit': 'microseconds', 'statistic': 'median of individual measured kernel end-start durations',
                'fixed_jac_layout': 'Predicted', 'dtype': 'int64',
                'primary_source_run_id': 'codegen/paired-profile', 'sources': sources,
                'input_manifest_sha256': profile['input_sha256'],
                'all_outputs_and_statuses_verified': True, 'cases': []}
        if key.startswith('jac'):
            label = 'O2' if key == 'jac_optimized' else ''
            data['ptx_sha256'] = profile['jac_variants'][label]['sha256']
            data['safety_contract'] = 'Full production named-cursor checks and status semantics'
        else:
            data['cuda_source_sha256'] = profile['cuda_source_sha256']
            data['kernel'] = 'matmul_tiled_i64'
        for case in profile['cases']:
            data['cases'].append({'case': case['id'], 'shape_M_K_N': case['shape'],
                'expected_sha256': case['expected_sha256'], **summaries[(case['id'], arm)],
                'kernel_samples': [x for x in verified['samples'] if x['case'] == case['id'] and x['arm'] == arm],
                'ordinary_event_samples': [x for x in ordinary['records'] if x['case'] == case['id'] and x['arm'] == arm]})
        datasets[key] = data
        write(primary / (key + '.json'), data)
    for case in profile['cases']:
        comparisons.append({'case': case['id'], 'M': case['shape'][0], 'K': case['shape'][1], 'N': case['shape'][2],
            **{key+'_us': summaries[(case['id'], arm)]['kernel_median_us'] for key, arm, _ in groups}})
    write(primary / 'comparison.json', {'unit': 'microseconds', 'statistic': 'median measured actual kernel duration',
        'source_run_id': 'codegen/paired-profile', 'fixed_jac_layout': 'Predicted',
        'groups': {key: desc for key, _, desc in groups}, 'sources': sources, 'comparisons': comparisons})
    with (primary / 'comparison.csv').open('w', newline='') as stream:
        fields = ['case', 'M', 'K', 'N', 'jac_original_us', 'jac_optimized_us', 'handwritten_us', 'unit', 'source_run_id']
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for row in comparisons:
            writer.writerow({**row, 'unit': 'microseconds', 'source_run_id': 'codegen/paired-profile'})

    lines = [
        '# Jac matmul: original, optimized, and handwritten CUDA', '',
        'The primary comparison has exactly three implementations. Both Jac columns use the **same Predicted packed graph layout**, lane order, inputs and launch geometry. The optimized column adds the **standard LLVM O2 middle-end pipeline** to the identical raw production LLVM module, verifies it, then emits PTX with the existing target machine. It retains the complete walker ABI, queues, type dispatch, arithmetic/bounds checks and status behavior. The scripts provide an explicit reproducible experimental compilation path; the production compiler keeps its current behavior.', '',
        '**Original Jac** uses the production backend and its existing target-machine optimization/code generation settings. **Optimized Jac** adds the checked LLVM O2 middle-end experimentally. **Handwritten** uses the same `matmul_tiled_i64` 16×16 shared-memory kernel across all five shapes, including the ragged cases.', '',
        '## Primary result: resident, actual kernel time', '',
        'Microseconds per kernel, median Nsight Systems `end - start`. All three columns come from **one interleaved run**, `codegen/paired-profile`, with randomized arm order in each round (seed 928), 3 warmup rounds and 15 measured rounds × 16 graph nodes per arm/case. Each cell contains 240 measured kernel samples. These durations exclude GPU graph scheduling gaps, CPU work, allocations and transfers.', '',
        '| M × K × N | Jac original | Jac with checked LLVM O2 | Handwritten tiled CUDA |',
        '|---|---:|---:|---:|']
    for row in comparisons:
        lines.append(f"| {row['M']} × {row['K']} × {row['N']} | {row['jac_original_us']:.3f} | {row['jac_optimized_us']:.3f} | {row['handwritten_us']:.3f} |")
    last = comparisons[-1]
    lines += ['', f"At 256³, compiler optimization gives **{last['jac_original_us']/last['jac_optimized_us']:.2f}×** speedup. Checked optimized Jac remains **{last['jac_optimized_us']/last['handwritten_us']:.2f}×** slower than the fixed handwritten tiled kernel. Both Jac measurements retain the full production graph execution contract.", '',
        'Download the [compact CSV](primary/comparison.csv), [comparison JSON with exact source hashes](primary/comparison.json), and three concrete datasets: [original Jac](primary/jac_original.json), [checked optimized Jac](primary/jac_optimized.json), [handwritten CUDA](primary/handwritten.json). Each dataset includes individual profiler samples and the separate ordinary-event samples. The source-run identifiers and SHA-256 hashes identify the exact interleaved run for every sample.', '',
        '## Why the original kernel is slow: supported findings', '',
        '1. **A removable compiler cost is established.** Production emission verifies LLVM and emits PTX directly through the existing target machine. The raw cursor lowering places ten fixed scalar allocas in `start`, after the lane-bound branch. SROA alone leaves IR/PTX unchanged (identical PTX SHA-256). Hoisting only those nonescaping fixed allocas to `entry` and running SROA removes all ten allocas and all 20 static local loads plus 20 static local stores in PTX. This checked ablation nearly reproduces O2 performance. Actual driver-JIT function attributes change from 80 local bytes and 28 registers per thread to zero local bytes and 40 registers, confirming that the static assembly observation applies to the loaded kernels. Offline `ptxas` reports zero spill loads/stores in every variant: the original frame is explicit local storage, with zero register spills reported.', '',
        '2. **General graph execution remains after compiler optimization.** O2 executes generic per-cursor FIFO traversal, CSR offset/target lookups, type dispatch, overflow and validation paths. Restricted chain controls execute much faster on regular layouts, but they accept a narrower contract and use a different compiler. Their measured speedups compare those complete implementations; attribution to queues and checks individually remains unresolved.', '',
        '3. **Checks have interacting, layout-dependent effects.** Separate LLVM ablations bypass only overflow errors, only graph/limit errors, or both. Some improve regular layouts; removing all checks actually slows the random layout in this experiment. These transformations alter subsequent optimization and register allocation. The timings compare complete generated implementations; attribution to individual check costs remains unresolved. The checked optimized variant retains the production safety contract.', '',
        '4. **Traversal representation matters, with non-monotonic controls.** Replacing CSR with one successor per node speeds the restricted chain kernel. A precomputed index schedule is faster than that successor kernel on Random928 but slower on regular layouts. The schedule also changes index organization and loop termination. Hardware-level attribution to cache misses, coalescing, occupancy and dependent-load latency remains unresolved.', '',
        'The [supplementary ablation report](codegen/ABLATIONS.md) gives every controlled change, its restricted contract, all five shapes and all layouts. The [earlier dense baseline report](DENSE_BASELINES.md) retains the original pre-ablation comparison.', '',
        '## Independent correctness and measurement checks', '',
        '- Real Jac Scalar/RowNext/ColumnNext objects were packed by the production packer. Each node stores one int64 value. The saved input manifest and every binary array hash are checked. Every cursor chain is walked on the CPU and checked against the dense A/B matrices before GPU measurement.',
        '- All five shapes compute the full M×N output, including negative values and ragged dimensions, with a NumPy int64 oracle. |A| ≤ 3, |B| ≤ 5 and |partial sum| ≤ 15K, so products and partial sums fit signed int64. Dense CUDA uses these same values and int64 arithmetic.',
        '- Before every graph replay, output is poisoned with the bitwise complement of its expected value and status with `0xffffffff`, outside timing. After each replay all outputs are checked; every Jac/graph-control lane must return zero status.',
        f"- The primary profiler join verified all **{verified['launches_verified']:,}** launches, including prime and warmup launches; **{verified['measured_launches']:,}** were measured. The separate ablation join verified **{ablation['launches_verified']:,}** launches; **{ablation['measured_launches']:,}** were measured. Every name, order, grid and block matches the runner request. `--cuda-graph-trace=node` was used in both runs.",
        '- Thirteen valid/error fixtures × three checked variants (baseline/O2/hoist+SROA), 39 standalone GPU launches, match the unmodified production host LLVM JIT exactly on output and status. Cases include multiply and add overflow, negative/out-of-range heads, invalid edge target, negative/overlarge CSR offsets, seed/branch queue overflow, cyclic round limit, type mismatch and empty channel. Failing lanes leave the poisoned result untouched. See [status validation](codegen/status-validation.json).',
        '- The existing named-cursor CPU/JIT suite passes all 15 tests, including FIFO branching/repeated arrivals, conditional visitation, reports, cycles, overflow, shared matmul inputs and dynamic cursor counts. This is supporting coverage of the unchanged backend; the direct 39 GPU comparisons exercise the checked experimental variants.', '',
        '## Separate ordinary CUDA-event cross-check', '',
        'Same three groups, from `codegen/paired-ordinary`: 5 warmup and 25 measured rounds, 16 graph nodes per replay. Microseconds per invocation; these event intervals **include** GPU graph scheduling gaps. The primary table uses the separately measured actual kernel durations.', '',
        '| M × K × N | Jac original | Jac with checked LLVM O2 | Handwritten tiled CUDA |',
        '|---|---:|---:|---:|']
    for case in profile['cases']:
        vals = [ordinary_cases[case['id']]['arms'][arm]['median_us'] for _, arm, _ in groups]
        lines.append('| ' + ' × '.join(map(str, case['shape'])) + ' | ' + ' | '.join(f'{v:.3f}' for v in vals) + ' |')
    lines += ['', '## Environment and reproduction', '',
        'RTX 3090, driver 580.65.06, CUDA 12.9 nvcc/ptxas, bundled Jac LLVM with NVPTX. Ollama held approximately 23,462 MiB in the before/after snapshots; only about 370 MB was free after our context. These are **shared-GPU measurements**. Per-run before/after snapshots are embedded in `results.json`. Nsight instrumentation and shared GPU state can shift absolute timing; primary ratios use one interleaved run and the ordinary cross-check is separate.', '',
        'Run [reproduce_codegen.sh](../../reproduce_codegen.sh) from the repository root to regenerate LLVM/PTX, both timing runs, profiler joins, error/status validation and report exports. GPU access is required. The original input arrays are reused unchanged. The script uses the current runner; the exact source revisions used by the earlier primary run are also saved as `codegen/paired-benchmark.py` and `codegen/paired-analyze_profile.py`, with hashes checked by the report generator. [commands.txt](codegen/commands.txt) records the invocation sequence and experimental identities.', '']
    (root / 'REPORT.md').write_text('\n'.join(lines))

    als = {(x['case'], x['arm']): x for x in ablation['summaries']}
    lines = ['# Supplementary compiler and traversal ablations', '',
        'Source run: `ablation-profile`, a separate interleaved run from the three-way primary table. Values below are median actual Nsight kernel microseconds (240 measured nodes per cell). `ablation-ordinary/results.json` supplies the independent event samples. Time differences compare independently optimized implementations. Attribution to individual mechanism costs remains unresolved.', '',
        '## Compiler transformations', '',
        '| Variant | Controlled change | Safety contract |', '|---|---|---|',
        '| baseline | Existing production target emission | Full production |',
        '| sroa | SROA only, unmodified raw module; assembly-equivalent baseline control | Full production |',
        '| hoist_sroa | Hoist ten fixed scalar allocas from start to entry; SROA only | Full production |',
        '| O2 | Standard LLVM O2 pipeline on the same raw module | Full production |',
        '| O2_no_overflow | Bypass the two error.3 branches, then O2 | Diagnostic: bounded arithmetic only |',
        '| O2_no_validation | Bypass errors 1/2/5/6, then O2; retain overflow and type dispatch | Diagnostic: valid finite graph/queue/round inputs only |',
        '| O2_unchecked | Bypass all thirteen error branches above, then O2; retain generic FIFO and type dispatch | Diagnostic: both restrictions above |', '',
        'All variants share the graph ABI and exact packed layout. `diagnose_codegen.py` saves the raw `input.ll`, each pre-codegen transformed IR, PTX, cubin, ptxas command/log and hashes. `emit_assembly` itself mutates its input IR; the raw module is captured before any emission. The benchmark loads PTX through the CUDA driver; cubins provide static diagnostic assembly evidence. Actual driver-JIT attributes are saved in `status-validation.json`.', '',
        '| Variant | LLVM allocas | PTX local loads/stores (static sites) | ptxas stack bytes | ptxas registers |', '|---|---:|---:|---:|---:|']
    import re
    for label, info in codegen['transformations'].items():
        stack = re.search(r'(\d+) bytes stack frame', info['ptxas']).group(1)
        regs = re.search(r'Used (\d+) registers', info['ptxas']).group(1)
        lines.append(f"| {label} | {info['IR_alloca_instructions']} | {info['PTX_local_loads']}/{info['PTX_local_stores']} | {stack} | {regs} |")
    lines += ['', '## Restricted graph controls', '',
        'Host preconditions: exactly one Scalar seed per channel, zero initial total, both chains of exactly K nodes, degree 0/1, finite traversal, valid indices and bounded products/sums. The benchmark checks every chain value and type; it proves schedule compression preserves each lane’s actual node identities. Every control computes the same complete matmul and writes status zero; all replay outputs/statuses are poisoned and checked. The general walker additionally supports branching, repeated arrivals, arbitrary seeds, invalid-input reporting and overflow detection.', '',
        '- `chain_csr`: NVCC implementation on the original packed values/CSR/heads; two register cursors, no FIFO or dynamic type/error machinery. Comparison with O2_unchecked measures the combined effect of specialization and compiler choice.',
        '- `chain_next`: same restricted chain computation and lane geometry, but replace four CSR-offset plus two target load sites per round with two direct successor lookups, including -1 termination. The CPU derives the successor table from the exact packed CSR; node/value layout is held fixed. The transform changes lookup count and address dependencies together.',
        '- `schedule`: precompute q-major A/B node-ID sequences from those same chains; keep original packed values and lane order. It replaces dynamic successors/termination with index loads and a K loop; its index organization and control flow differ from `chain_next`.',
        '- `CUDA flat`: dense address arithmetic with the graph arms’ 128-thread one-dimensional geometry and lane order, and `#pragma unroll 1`, matching the schedule kernel’s loop policy. Dense naive/tiled use 256-thread 16×16 geometry and their own compiled loops. Flat versus naive compares both launch geometry and compiled loop policy.', '',
        '## Actual kernel measurements', '']
    for case in ablation_results['cases']:
        lines += ['### ' + ' × '.join(map(str, case['shape'])), '',
                  '| Implementation | Current | Predicted | Random928 |', '|---|---:|---:|---:|']
        for variant in ['', 'O2', 'hoist_sroa', 'O2_no_overflow', 'O2_no_validation', 'O2_unchecked']:
            vals = [als[(case['id'], 'Jac '+(variant+' ' if variant else '')+layout)]['kernel_median_us'] for layout in ['Current', 'Predicted', 'Random-928']]
            lines.append('| Jac '+(variant or 'baseline')+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
        for name in ['chain_csr', 'chain_next', 'schedule']:
            vals = [als[(case['id'], 'Graph '+name+' '+layout)]['kernel_median_us'] for layout in ['Current', 'Predicted', 'Random-928']]
            lines.append('| Graph '+name+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
        for name in ['naive', 'tiled', 'flat']:
            val = als[(case['id'], 'CUDA '+name)]['kernel_median_us']
            lines.append(f'| Dense CUDA {name} | {val:.3f} | — | — |')
        lines.append('')
    cid = 'matmul-256x256x256'
    get = lambda arm: als[(cid, arm)]['kernel_median_us']
    lines += ['## Interpretation and unresolved attribution', '',
        f"At 256³ Predicted, baseline {get('Jac Predicted'):.3f} → hoist+SROA {get('Jac hoist_sroa Predicted'):.3f} µs closely matches O2 {get('Jac O2 Predicted'):.3f} µs. At 3×5×2 and 17×31×19 the relative compiler improvement is smaller. The measured promotion benefit varies with matrix size.", '',
        f"On Predicted 256³, O2_no_overflow is {get('Jac O2_no_overflow Predicted'):.3f}, O2_no_validation {get('Jac O2_no_validation Predicted'):.3f}, and O2_unchecked {get('Jac O2_unchecked Predicted'):.3f} µs. On Random928, however, checked O2 is {get('Jac O2 Random-928'):.3f} versus unchecked {get('Jac O2_unchecked Random-928'):.3f} µs; the ordinary-event run also shows the reversal. Deleting validation changes optimized PTX (including 17→21 static global-load sites and 6→10 global-store sites), and the overflow variants use different register counts. The hardware cause of the reversal remains unresolved. Static instruction sites describe generated code; dynamic transaction counts require separate measurements.", '',
        f"On Predicted, chain_next {get('Graph chain_next Predicted'):.3f} is faster than schedule {get('Graph schedule Predicted'):.3f} µs; on Random928, chain_next {get('Graph chain_next Random-928'):.3f} is slower than schedule {get('Graph schedule Random-928'):.3f} µs. The ordinary run corroborates both directions. The faster representation depends on layout. This control changes address streams and termination together, leaving their individual hardware contributions unresolved.", '',
        'Current and Predicted are close on the large regular case, while Random928 is slower for multiple graph implementations. This establishes sensitivity to physical representation at fixed graph semantics. Cache hit rate, coalescing efficiency and occupancy remain unmeasured: earlier Nsight Compute access returned `ERR_NVGPUCTRPERM`.', '',
        'The checked optimization path is experimental; the unchecked and restricted-chain paths serve as diagnostic controls.', '']
    (base / 'ABLATIONS.md').write_text('\n'.join(lines))
    print('Verified source hashes and generated REPORT.md, ABLATIONS.md and three primary datasets.')


if __name__ == '__main__':
    main()
