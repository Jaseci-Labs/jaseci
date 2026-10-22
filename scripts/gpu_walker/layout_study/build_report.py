#!/usr/bin/env python3
"""Check the O2 layout contract, saved evidence, and export the three primary groups."""
import argparse
import csv
from pathlib import Path
from prepare import HERE, ROOT, read, write, get, sha
from run import BEFORE, AFTER, REFERENCE


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('validation', type=Path)
    v = p.parse_args().validation
    contract = HERE/'RESEARCH_CONTRACT.md'
    for label in ['**Jac before (Random + checked LLVM O2):**', '**Jac after (Predicted + checked LLVM O2):**', '**Handwritten CUDA reference:**']:
        assert label in contract.read_text()
    profile = v/'optimized-profile'
    r = read(profile/'results.json')
    checked = read(profile/'verified.json')
    ordinary = read(v/'optimized-ordinary/results.json')
    inputs = read(v/'inputs/inputs.json')
    cg = read(v/'optimized-codegen/codegen.json')
    model = read(v/'optimized-address-analysis.json')
    counter = read(v/'counters/o2-status.json')
    status_path = ROOT/cg['status_evidence']
    status = read(status_path)
    assert status['status'] == 'PASS' and sha(status_path) == cg['status_evidence_sha256']
    assert status['ptx_sha256']['O2'] == cg['optimized_ptx_sha256']
    assert all(c['variants']['O2']['pass'] for c in status['cases'])
    assert cg['generator_sha256'] == sha(HERE/'emit_checked_o2.py')
    for path, digest in cg['compiler_source_sha256'].items():
        assert sha(ROOT/path) == digest
    assert cg['production_ptx_sha256'] == inputs['ptx_sha256'] == sha(v/'inputs/Dot.ptx')
    assert cg['optimized_ptx_sha256'] == sha(v/'optimized-codegen/O2.ptx')
    assert cg['raw_ir_sha256'] == sha(v/'optimized-codegen/raw.ll')
    assert cg['optimized_ir_sha256'] == sha(v/'optimized-codegen/O2.ll')
    assert checked['status'] == 'PASS' and checked['analyzer_sha256'] == sha(HERE/'analyze.py')
    assert checked['results_sha256'] == sha(profile/'results.json')
    assert checked['sqlite_sha256'] == sha(profile/'trace.sqlite')
    assert inputs['generator_sha256'] == sha(HERE/'prepare.py')
    assert inputs['source_jac_sha256'] == sha(ROOT/'jac/examples/gpu/named_cursors.jac')
    assert inputs['source_manifest_sha256'] == sha(ROOT/inputs['source_manifest'])
    assert model['source_sha256'] == sha(HERE/'address_analysis.py')
    assert model['input_sha256'] == sha(v/'inputs/inputs.json')
    assert model['profile_results_sha256'] == sha(profile/'results.json')
    for run in [r, ordinary]:
        assert run['complete'] and run['primary_arms'] == [BEFORE, AFTER, REFERENCE]
        assert run['runner_sha256'] == sha(HERE/'run.py')
        assert run['prepare_sha256'] == sha(HERE/'prepare.py')
        assert run['driver_sha256'] == sha(HERE.parent/'handwritten_matmul/benchmark.py')
        assert run['contract_sha256'] == sha(contract)
        assert run['input_manifest_sha256'] == sha(v/'inputs/inputs.json')
        assert run['optimized_codegen_sha256'] == sha(v/'optimized-codegen/codegen.json')
        assert run['jac_ptx_sha256'] == cg['optimized_ptx_sha256']
        assert run['jac_function_loaded_once_for_all_layouts']
        assert run['reference_kernel'] == 'matmul_tiled_i64'
        assert run['reference_source_sha256'] == sha(HERE.parent/'handwritten_matmul/matmul.cu')
        assert '-O3' in run['nvcc_command']
        assert all(record['all_outputs_and_statuses_checked'] for record in run['records'])
        for case in run['cases']:
            assert case['all_outputs_and_statuses_verified'] and case['all_node_permutations_and_logical_traversals_verified']
            for field in ['kernel', 'grid', 'block']:
                assert case['arms'][BEFORE][field] == case['arms'][AFTER][field]
    for directory, run in [(profile, r), (v/'optimized-ordinary', ordinary)]:
        assert sha(directory/'matmul.ptx') == run['reference_ptx_sha256']
    assert r['reference_ptx_sha256'] == ordinary['reference_ptx_sha256']
    for case in inputs['cases']:
        folder = v/'inputs'/case['id']
        get(folder, case['expected'])
        capacities, bounds = set(), set()
        for layout in case['layouts']:
            get(folder, layout['identity_order'])
            for info in layout['files']:
                get(folder, info)
            assert layout['audit']['all_node_fields_edges_heads_and_queue_remap_verified']
            assert layout['audit']['all_lane_cursor_arrivals_logically_identical']
            capacities.add(layout['queue_capacity']); bounds.add(layout['max_visits'])
        assert len(capacities) == len(bounds) == 1
    lookup = {(s['case'], s['arm']): s for s in checked['summaries']}
    rows, seeds, variability, events = [], [], [], []
    for case in r['cases']:
        cid = case['id']
        b, a, ref = [lookup[cid, arm]['median_us'] for arm in [BEFORE, AFTER, REFERENCE]]
        rows.append({'case': cid, 'M': case['shape'][0], 'K': case['shape'][1], 'N': case['shape'][2],
            'jac_before_random928_o2_us': b, 'jac_after_predicted_o2_us': a,
            'handwritten_cuda_o3_reference_us': ref,
            'layout_speedup_before_after': b/a, 'residual_gap_after_reference': a/ref})
        for seed, arm in [(928, BEFORE), (929, 'Random929 robustness'), (930, 'Random930 robustness')]:
            entry = lookup[cid, arm]
            seeds.append({'case': cid, 'seed': seed, 'before_us': entry['median_us'], 'after_us': a,
                'speedup': entry['median_us']/a, 'sample_n': entry['sample_n'],
                'paired_round_mean_speedups': [x/y for x,y in zip(entry['pair_mean_us'], lookup[cid, AFTER]['pair_mean_us'])]})
        for arm in [BEFORE, AFTER, REFERENCE]:
            variability.append({k: lookup[cid, arm][k] for k in ['case', 'arm', 'median_us', 'p10_us', 'p90_us', 'min_us', 'max_us', 'sample_n']})
        event_case = next(c for c in ordinary['cases'] if c['id'] == cid)
        eb, ea, er = [event_case['arms'][arm]['median_event_us'] for arm in [BEFORE, AFTER, REFERENCE]]
        events.append({'case': cid, 'before_us': eb, 'after_us': ea, 'reference_us': er, 'layout_speedup': eb/ea})
    source_names = ['inputs/inputs.json', 'inputs/Dot.ptx', 'optimized-codegen/O2.ptx', 'optimized-codegen/codegen.json',
        'optimized-profile/results.json', 'optimized-profile/verified.json', 'optimized-profile/trace.sqlite', 'optimized-profile/trace.nsys-rep',
        'optimized-ordinary/results.json', 'optimized-address-analysis.json', 'counters/o2-ncu.log', 'counters/o2-status.json']
    sources = {name: sha(v/name) for name in source_names}
    write(v/'comparison.json', {'contract_sha256': sha(contract), 'primary_groups': [BEFORE, AFTER, REFERENCE],
        'jac_independent_variable': 'node layout only; same checked LLVM O2 PTX', 'unit': 'microseconds',
        'statistic': 'median actual Nsight kernel end-start', 'source_run_id': 'optimized-profile', 'sources_sha256': sources, 'rows': rows})
    with (v/'comparison.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[*rows[0], 'unit', 'source_run_id'], lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, 'unit': 'microseconds', 'source_run_id': 'optimized-profile'})
    write(v/'seed-robustness.json', {'source_run_id': 'optimized-profile', 'unit': 'microseconds', 'primary_seed': 928, 'seeds': seeds})
    write(v/'variability.json', {'source_run_id': 'optimized-profile', 'unit': 'microseconds', 'primary_distributions': variability, 'ordinary_events': events})
    oldbase = ROOT/'scripts/gpu_walker/large_matmul/validation'
    full, old, identity = [read(oldbase/name) for name in ['full-run.json', 'profile.json', 'identity-audit.json']]
    assert full['complete'] and full['full_outputs'] == 9000000 and not old['full_result'] and old['batch'] == 32768
    assert identity['complete_A_then_complete_B']
    dist = old['summary'][0]['distributions']['kernel_profiler_us']
    graph_bytes, free = 719952016, r['memory_before']['free']
    scale = {'shape': [3000,3000,3000], 'historical_full_outputs_checked': full['full_outputs'], 'historical_timed_outputs_per_launch': old['batch'],
        'historical_subset_random_us': dist['Random']['median'], 'historical_subset_predicted_us': dist['Predicted']['median'],
        'historical_subset_speedup': dist['Random']['median']/dist['Predicted']['median'], 'historical_handwritten_reference': 'absent',
        'historical_ptx_sha256': old['PTX_sha256'], 'graph_bytes_per_layout': graph_bytes, 'current_free_bytes_after_context': free,
        'two_graphs_dense_full_matrices_and_bounded_private_lower_bytes': 2*graph_bytes+3*3000*3000*8+2*32768*68,
        'resident_graph_feasible_now': graph_bytes <= free, 'historical_raw_dir_currently_exists': Path('/tmp/jac-large-matmul-3000-20261007').exists(),
        'historical_sources_sha256': {str(p.relative_to(ROOT)): sha(p) for p in [oldbase/'full-run.json', oldbase/'profile.json', oldbase/'identity-audit.json', ROOT/'docs/design/gpu-large-matmul-3000-results.md']}}
    write(v/'scale-3000-feasibility.json', scale)
    seg = {(x['case'],x['layout'],x['cursor'],x['logical_load']):x for x in model['summaries']}
    largest = rows[-1]
    lines = ['# Jac GPU layout: checked O2 Random before, Predicted after, tiled CUDA reference', '',
        f"Access-order-aware layout changes the 256³ Jac median from {largest['jac_before_random928_o2_us']:.3f} to {largest['jac_after_predicted_o2_us']:.3f} µs: **{largest['layout_speedup_before_after']:.3f}× faster**. The remaining Predicted / tiled CUDA gap is **{largest['residual_gap_after_reference']:.2f}×**. Predicted regresses on the two smallest cases and improves the three larger cases across all three fixed random seeds.", '',
        '## Primary policy and exact invariants', '',
        '- **Jac before (Random928 + checked LLVM O2):** shuffled physical node IDs, consistently remapping fields, CSR rows/targets, heads and initialized queues.',
        '- **Jac after (Predicted + identical checked LLVM O2):** complete cursor-a discovery BFS followed by complete cursor-b discovery BFS, preserving first occurrence: all A nodes, then all B nodes.',
        '- **Handwritten CUDA reference (nvcc O3):** fixed `matmul_tiled_i64` 16×16 shared-memory tiled int64 kernel for every size, covering the same logical matrices and all outputs.', '',
        'The Jac independent variable is **node layout only**. Both Jac arms reuse one loaded function and byte-identical checked O2 PTX. Source, arithmetic, logical graph identities/values/edges, lane order, walker-to-thread mapping, queue capacity, visit bound, initial state, output coverage and launch geometry are fixed. Jac uses block=(128,1,1), grid=(ceil(MN/128),1,1); CUDA uses block=(16,16,1), grid=(ceil(N/16),ceil(M/16),1).', '',
        'Jac receives the standard LLVM O2 middle-end pipeline on the exact production raw module, followed by the existing target codegen. The reference receives nvcc `-O3 -arch=compute_86 -std=c++17`. Both receive regular optimizing pipelines; LLVM O2 and nvcc O3 are distinct pipelines with different optimization guarantees. The explicit checked O2 compilation path is experimental. The [research contract](../../RESEARCH_CONTRACT.md) and its recorded hash define the primary policy.', '',
        f"**Checked O2 PTX SHA-256:** `{r['jac_ptx_sha256']}`. The [emitter](../../emit_checked_o2.py) first verifies that production emission matches the saved production PTX (`{cg['production_ptx_sha256']}`), then optimizes that same raw LLVM. [Codegen provenance](optimized-codegen/codegen.json) includes IR/compiler hashes and offline ptxas output: zero stack bytes, zero spills, 40 registers. Safety checks/status paths are retained.", '',
        '## Fresh primary result: full output coverage', '',
        '**Median actual Nsight node-kernel end−start, microseconds.** All cells come from one randomized interleaved `optimized-profile` run. Random928 is the prespecified primary seed; Random929/930 provide supporting repetitions in the same run. Each cell contains 240 measured nodes (15 rounds × 16 sequential graph nodes), after three warmup rounds. Independent arm-order seed: 237.', '',
        '| M × K × N | Jac before: Random928 + O2 | Jac after: Predicted + O2 | Handwritten tiled CUDA O3 | Layout speedup before/after | Residual gap after/reference |',
        '|---|---:|---:|---:|---:|---:|']
    fields = ['jac_before_random928_o2_us','jac_after_predicted_o2_us','handwritten_cuda_o3_reference_us']
    for row in rows:
        lines.append('| '+' × '.join(str(row[k]) for k in ['M','K','N'])+' | '+' | '.join(f'{row[k]:,.3f}' for k in fields)+f" | {row['layout_speedup_before_after']:.3f}× | {row['residual_gap_after_reference']:.2f}× |")
    lines += ['', '[Compact CSV](comparison.csv) · [JSON with exact source-run hashes](comparison.json) · [all actual kernel samples and launch join](optimized-profile/verified.json). Every kernel covers the full M×N output workload.', '',
        f"The independent launch audit matched **{checked['launches_verified']:,}** launches, including primes and warmups, with **{checked['measured_launches']:,}** measured nodes; 3,600 measured nodes belong to the three primary groups. Every kernel name, order, grid, block and graph-node position matches the request. Nsight uses `--cuda-graph-trace=node`.", '',
        '### Variability and fixed seeds', '',
        '| Shape | Random928 / Predicted | Random929 / Predicted | Random930 / Predicted |', '|---|---:|---:|---:|']
    for case in r['cases']:
        selected = [x for x in seeds if x['case'] == case['id']]
        lines.append('| '+' × '.join(map(str,case['shape']))+' | '+' | '.join(f"{x['speedup']:.3f}×" for x in selected)+' |')
    lines += ['', 'All three fixed seeds give the same direction at every size. [Seed data](seed-robustness.json) include each round’s paired mean ratio. [Variability data](variability.json) retain p10/p90, minima/maxima and separate ordinary-event medians; raw traced samples are retained.', '',
        '| 256³ primary group | p10 µs | median µs | p90 µs |', '|---|---:|---:|---:|']
    for arm in [BEFORE, AFTER, REFERENCE]:
        s = lookup[r['cases'][-1]['id'],arm]
        lines.append(f"| {arm} | {s['p10_us']:.3f} | {s['median_us']:.3f} | {s['p90_us']:.3f} |")
    e = events[-1]
    lines += ['', f"The separate ordinary-event run uses 5 warmup rounds and 25 measured rounds × 16 nodes, checking every replay. Its 256³ medians are {e['before_us']:.3f} / {e['after_us']:.3f} / {e['reference_us']:.3f} µs, giving {e['layout_speedup']:.3f}× layout speedup. All five sizes have the same direction as the primary trace. Event intervals include graph scheduling gaps and come from a separate run; primary ratios use actual kernel times from `optimized-profile`.", '',
        '## Full semantics and identity checks', '',
        'The saved fixtures originate from real Jac Scalar/RowNext/ColumnNext objects and the production packer. Canonical discovery identities anchor the remapping. Predicted is independently reconstructed from complete lane chains as all-A BFS then all-B BFS. Each permutation is a full bijection. Every field/tag, CSR row/target, head and initialized queue is checked against the canonical graph, and every q/cursor/lane arrival is checked for the same logical identity. Array and permutation SHA-256 hashes are saved. The runner repeats these audits before GPU execution.', '',
        'Before every replay, outside timing, output is poisoned with the bitwise complement of its expected value and Jac status with `0xffffffff`. Every M×N result is checked against independent NumPy int64 A@B and the saved full-output oracle; every Jac status must be zero. Input magnitudes bound every product by 15 and every partial sum by 15K. Supporting random seeds receive the same checks.', '',
        f"The identical O2 artifact also passed the earlier direct GPU [status validation](../../../handwritten_matmul/validation/20261021/codegen/status-validation.json), SHA-256 `{cg['status_evidence_sha256']}`: 13 fixtures covering multiply/add overflow, round-limit cycles, queue capacity, invalid heads/targets/CSR, type mismatch, empty channel and valid execution. Each matched the production host JIT’s exact result/status; baseline, O2 and checked hoist+SROA totalled 39 passing executions. This report verifies the O2 artifact hash against that evidence. Fresh normal-case replays verify all outputs/statuses for every layout.", '',
        '## Measured layout effect and address evidence', '',
        'The controlled Random/Predicted timing difference establishes the layout effect under this workload and shared GPU context. The residual gap to tiled CUDA compares complete implementations: the graph kernel retains traversal queues, CSR lookup, dispatch and checks, while tiled CUDA uses dense indexing and cooperative shared-memory reuse. Component contributions to that whole-implementation gap remain unresolved.', '',
        'The corrected O2 Nsight Compute probe requested `l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum` and returned **ERR_NVGPUCTRPERM**, exit 1. [Exact log](counters/o2-ncu.log) and [status](counters/o2-status.json) retain the access limitation. The probe is separate from primary timings.', '',
        'The [deterministic address analysis](optimized-address-analysis.json) uses the exact layouts and actual 256-byte-aligned device array bases from the primary run. For each q, cursor and logical value/tag/CSR load, it counts distinct 32-byte address segments per logical warp access, merges duplicate lane addresses, and retains per-q statistics, count-vector hashes and example adjacent-lane addresses. These are deterministic address counts. Hardware transactions, cache misses and occupancy remain unmeasured; compiler load transformations and cache state are outside this model.', '',
        '| 256³ logical warp access: mean distinct 32-byte segments | Random928 | Predicted |', '|---|---:|---:|']
    for cursor, load in [('a','value'),('b','value'),('b','csr_begin'),('b','csr_end'),('b','csr_target')]:
        b, a = [seg['matmul-256x256x256',layout,cursor,load]['mean_segments'] for layout in ['before','after']]
        lines.append(f'| cursor {cursor}: {load} | {b:.3f} | {a:.3f} |')
    lines += ['', 'At N=256 a warp covers one row i and 32 adjacent columns j. Cursor a shares one A-node address across the warp in either layout. Cursor b visits 32 distinct nodes; Predicted places them consecutively, giving eight value-address segments versus about 32 with Random928. CSR begin/end indexing also includes the channel-row offset. Jac’s known cursor order therefore supports a concrete, reproducible address organization. Timings show useful speedup for larger cases and regression for small cases; the hardware mechanism behind those differences remains unresolved.', '',
        '## Shared GPU and timing boundary', '',
        f"RTX 3090, driver 580.65.06, CUDA 12.9. Ollama held approximately 23,462 MiB in the before/after snapshots. The process measured {free/1e6:.2f} MB free after context creation. The largest planned allocation for the five arms was {max(c['planned_device_bytes'] for c in r['cases'])/1e6:.2f} MB. Each case checks current free VRAM and releases buffers before the next case. Full snapshots and allocation plans are in `optimized-profile/results.json` and `optimized-ordinary/results.json`.", '',
        'Resident actual kernel intervals cover computation. Packing/remapping, compilation, allocation, transfers, output poisoning, verification and graph scheduling gaps are separate from this metric. Layout-construction cost is outside the resident-kernel measurement; the production input provenance and remapping scripts are retained. Absolute durations reflect this shared GPU context.', '',
        '## Supplementary production-PTX history and 3000³ feasibility', '',
        'The earlier [production-PTX confirmation](production-PTX-REPORT.md) and [same-trace pilot](../../pilot/comparison.json) are supplementary history using production emission before the added LLVM middle-end. The pilot’s 256³ Random928 / Predicted / tiled values were 4486.394 / 2069.116 / 20.608 µs. These data retain their own hashes, contract and source snapshot. The corrected primary table uses checked O2 for both Jac layouts and the new `optimized-profile` trace.', '',
        f"Historical 3000³ correctness covered **9,000,000 outputs**, with 27 billion multiply-accumulates. Separate historical actual timings covered **32,768 outputs per resident launch**: Random {scale['historical_subset_random_us']/1000:.3f} ms, Predicted {scale['historical_subset_predicted_us']/1000:.3f} ms, {scale['historical_subset_speedup']:.3f}× subset speedup. That run has its own older PTX/data and no handwritten reference. Full-result correctness and subset timing are separate evidence.", '',
        f"One 3000³ packed graph requires {graph_bytes/1e6:.2f} MB, exceeding the measured {free/1e6:.2f} MB free. Two layouts, dense full A/B/C, and bounded 32,768-query Jac buffers require approximately {scale['two_graphs_dense_full_matrices_and_bounded_private_lower_bytes']/1e9:.2f} GB before additional JIT/allocation headroom. Dense A/B/C alone occupy 216 MB. The historical temporary raw directory is currently absent; checked-in summaries, audits, hashes and source remain available.", '',
        'A matched full-coverage 3000³ follow-up can use a GPU/session with sufficient free VRAM, retain the paired graphs, execute all 275 bounded Jac batches covering nine million outputs, and compare aggregate actual kernel time with the fixed tiled reference over the same outputs. A matched 32,768-output subset study needs a tiled reference covering that exact selection and explicit subset labeling. Paging/partitioning introduces an out-of-core question. [Scale record and historical hashes](scale-3000-feasibility.json) preserve the resource and coverage boundary.', '',
        '## Reproduction and artifacts', '',
        '[Reproduction script](../../reproduce.sh) · [runner](../../run.py) · [input/permutation audit](../../prepare.py) · [checked O2 emitter](../../emit_checked_o2.py) · [profiler join](../../analyze.py) · [address analysis](../../address_analysis.py). The [English PDF](../../../../../docs/presentations/jac-gpu-layout/jac-gpu-layout.pdf) is generated from the verified comparison and contract. The optional subtree capture is retained with its paused status; matmul supplies this report’s primary results.', '']
    (v/'REPORT.md').write_text('\n'.join(lines))
    write(v/'contract-validation.json', {'status': 'PASS', 'contract_sha256': sha(contract), 'primary_groups': r['primary_arms'],
        'jac_variable': 'node layout only; same checked LLVM O2', 'identical_ptx': True, 'identical_jac_geometry': True,
        'logical_identity_audits': True, 'full_output_status_checks': True, 'checked_error_artifact_verified': True,
        'source_run_id': 'optimized-profile', 'profiler_launches_verified': checked['launches_verified'], 'report_generator_sha256': sha(Path(__file__))})
    print('PASS: checked-O2 contract, all source/input hashes, semantics evidence and profiler joins; primary exports complete.')


if __name__ == '__main__':
    main()
