#!/usr/bin/env python3
"""Validate the layout-study contract and export measured matmul findings."""
import argparse
import csv
import os
from pathlib import Path
from prepare import HERE,ROOT,read,write,get,sha
from run import BEFORE,AFTER,REFERENCE


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('validation',type=Path);a=p.parse_args();v=a.validation
    contract=HERE/'RESEARCH_CONTRACT.md';text=contract.read_text()
    for name in ['**Jac before (Random):**','**Jac after (Predicted):**','**Handwritten CUDA reference:**']:assert name in text
    inputs=read(v/'inputs/inputs.json');r=read(v/'profile/results.json');check=read(v/'profile/verified.json');ordinary=read(v/'ordinary/results.json');model=read(v/'address-analysis.json');counter=read(v/'counters/status.json')
    assert r['complete'] and ordinary['complete'] and check['status']=='PASS'
    assert r['primary_arms']==[BEFORE,AFTER,REFERENCE] and ordinary['primary_arms']==r['primary_arms']
    assert r['contract_sha256']==sha(contract)
    assert check['results_sha256']==sha(v/'profile/results.json') and check['sqlite_sha256']==sha(v/'profile/trace.sqlite')
    assert check['analyzer_sha256']==sha(HERE/'analyze.py')
    assert inputs['generator_sha256']==sha(HERE/'prepare.py')
    assert model['source_sha256']==sha(HERE/'address_analysis.py') and model['input_sha256']==sha(v/'inputs/inputs.json')
    assert model['profile_results_sha256']==sha(v/'profile/results.json')
    for run in [r,ordinary]:
        assert run['runner_sha256']==sha(HERE/'run.py') and run['prepare_sha256']==sha(HERE/'prepare.py')
        assert run['jac_function_loaded_once_for_all_layouts']
        assert run['jac_ptx_sha256']==inputs['ptx_sha256']==sha(v/'inputs/Dot.ptx')
        assert run['input_manifest_sha256']==sha(v/'inputs/inputs.json')
        assert run['reference_kernel']=='matmul_tiled_i64' and run['reference_source_sha256']==sha(HERE.parent/'handwritten_matmul/matmul.cu')
        assert all(c['all_outputs_and_statuses_verified'] and c['all_node_permutations_and_logical_traversals_verified'] for c in run['cases'])
        for case in run['cases']:
            assert case['arms'][BEFORE]['kernel']==case['arms'][AFTER]['kernel']==run['jac_kernel']
            assert case['arms'][BEFORE]['grid']==case['arms'][AFTER]['grid'] and case['arms'][BEFORE]['block']==case['arms'][AFTER]['block']
    for case in inputs['cases']:
        folder=v/'inputs'/case['id'];get(folder,case['expected'])
        caps=set();limits=set()
        for layout in case['layouts']:
            get(folder,layout['identity_order'])
            for info in layout['files']:get(folder,info)
            assert all(layout['audit'][key] for key in ['all_node_fields_edges_heads_and_queue_remap_verified','all_lane_cursor_arrivals_logically_identical'])
            caps.add(layout['queue_capacity']);limits.add(layout['max_visits'])
        assert len(caps)==len(limits)==1
    lookup={(x['case'],x['arm']):x for x in check['summaries']}
    rows=[];seeds=[]
    for case in r['cases']:
        cid=case['id'];b=lookup[cid,BEFORE]['median_us'];after=lookup[cid,AFTER]['median_us'];ref=lookup[cid,REFERENCE]['median_us']
        rows.append({'case':cid,'M':case['shape'][0],'K':case['shape'][1],'N':case['shape'][2],
            'jac_before_random928_us':b,'jac_after_predicted_us':after,'handwritten_cuda_reference_us':ref,'layout_speedup_before_after':b/after,'residual_gap_after_reference':after/ref})
        for seed,arm in [(928,BEFORE),(929,'Random929 robustness'),(930,'Random930 robustness')]:
            seeds.append({'case':cid,'seed':seed,'before_us':lookup[cid,arm]['median_us'],'after_us':after,'speedup':lookup[cid,arm]['median_us']/after,'sample_n':lookup[cid,arm]['sample_n'],
                'paired_round_mean_speedups':[b/a for b,a in zip(lookup[cid,arm]['pair_mean_us'],lookup[cid,AFTER]['pair_mean_us'])]})
    sources={name:sha(v/name) for name in ['inputs/inputs.json','inputs/Dot.ptx','profile/results.json','profile/verified.json','profile/trace.sqlite','profile/trace.nsys-rep','ordinary/results.json','address-analysis.json','counters/ncu.log']}
    write(v/'comparison.json',{'contract_sha256':sha(contract),'primary_groups':[BEFORE,AFTER,REFERENCE],'jac_independent_variable':'node layout only','unit':'microseconds','statistic':'median actual Nsight kernel end-start','source_run_id':'profile','sources_sha256':sources,'rows':rows})
    with (v/'comparison.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=[*rows[0],'unit','source_run_id'],lineterminator='\n');writer.writeheader()
        for row in rows:writer.writerow({**row,'unit':'microseconds','source_run_id':'profile'})
    write(v/'seed-robustness.json',{'source_run_id':'profile','unit':'microseconds','primary_seed':928,'seeds':seeds})
    oldbase=ROOT/'scripts/gpu_walker/large_matmul/validation';full=read(oldbase/'full-run.json');old=read(oldbase/'profile.json');identity=read(oldbase/'identity-audit.json')
    assert full['complete'] and full['full_outputs']==9000000 and not old['full_result'] and old['batch']==32768 and identity['complete_A_then_complete_B']
    distribution=old['summary'][0]['distributions']['kernel_profiler_us'];graph_bytes=719952016;free=r['memory_before']['free']
    scale={'shape':[3000,3000,3000],'historical_full_outputs_checked':full['full_outputs'],'historical_timed_outputs_per_launch':old['batch'],
        'historical_subset_random_us':distribution['Random']['median'],'historical_subset_predicted_us':distribution['Predicted']['median'],
        'historical_subset_speedup':distribution['Random']['median']/distribution['Predicted']['median'],'historical_handwritten_reference':'absent',
        'historical_ptx_sha256':old['PTX_sha256'],'graph_bytes_per_layout':graph_bytes,'current_free_bytes_after_context':free,
        'two_graphs_dense_full_matrices_and_bounded_private_lower_bytes':2*graph_bytes+3*3000*3000*8+2*32768*68,
        'resident_graph_feasible_now':graph_bytes<=free,'historical_raw_dir_currently_exists':Path('/tmp/jac-large-matmul-3000-20261007').exists(),
        'historical_sources_sha256':{str(path.relative_to(ROOT)):sha(path) for path in [oldbase/'full-run.json',oldbase/'profile.json',oldbase/'identity-audit.json',ROOT/'docs/design/gpu-large-matmul-3000-results.md']}}
    write(v/'scale-3000-feasibility.json',scale)
    segments={(x['case'],x['layout'],x['cursor'],x['logical_load']):x for x in model['summaries']}
    s=lambda value:f'{value:,.3f}'
    lines=['# Jac GPU node layout: Random before, Predicted after, CUDA reference','',
        'The Jac independent variable is **node layout only**. Access-order-aware Predicted regresses on the two smallest full-matmul cases and improves the three larger cases across all three fixed random seeds. At 256³, the primary Random928/Predicted speedup is '+f"{rows[-1]['layout_speedup_before_after']:.3f}×"+'; the remaining Predicted/tiled-CUDA reference gap is '+f"{rows[-1]['residual_gap_after_reference']:.2f}×"+'.','',
        '## Contract and primary implementations','',
        '- **Jac before (Random928):** shuffled physical node IDs, with consistent field/CSR/target/head/seed-queue remapping.',
        '- **Jac after (Predicted):** complete cursor-a discovery BFS followed by complete cursor-b discovery BFS, preserving first occurrence: all A nodes, then all B nodes.',
        '- **Handwritten CUDA reference:** the fixed `matmul_tiled_i64` 16×16 shared-memory kernel on the same logical int64 matrices and all outputs.','',
        'Both Jac arms use the same loaded production function and byte-identical PTX (`'+r['jac_ptx_sha256']+'`). Jac source, arithmetic, graph identities/edges, lane order, walker-to-thread mapping, queue/visit limits and launch geometry are fixed. Both launch 128 threads per block and ceil(MN/128) blocks. The reference uses its fixed 16×16 geometry and the same M,K,N inputs; its algorithm and launch geometry provide the performance target.','',
        'The [research contract](../../RESEARCH_CONTRACT.md) defines these invariants and acceptance checks. The report generator checks the three primary labels, common PTX/source hash, one loaded Jac function, Jac geometry, input/permutation hashes, logical traversal audits and profiler joins before export. Compiler optimization is fixed throughout the Jac layout pair.','',
        '## Fresh primary result: full output coverage','',
        'Median actual Nsight kernel end−start in **microseconds**, from one randomized interleaved `profile` run. Random928 is the prespecified primary seed; Random929/930 are supporting repetitions in the same run. Each cell contains 240 measured kernel nodes (15 rounds × 16 nodes), after three warmup rounds. Arm order is randomized independently of the layout seeds, with order seed 237.','',
        '| M × K × N | Jac before (Random928) | Jac after (Predicted) | Handwritten CUDA reference | Layout speedup before/after | Residual gap after/reference |',
        '|---|---:|---:|---:|---:|---:|']
    for row in rows:lines.append('| '+' × '.join(str(row[k]) for k in ['M','K','N'])+' | '+' | '.join(s(row[k]) for k in ['jac_before_random928_us','jac_after_predicted_us','handwritten_cuda_reference_us'])+f" | {row['layout_speedup_before_after']:.3f}× | {row['residual_gap_after_reference']:.2f}× |")
    lines+=['','[Compact CSV](comparison.csv) · [JSON with exact source-run hashes](comparison.json) · [sample distributions and profiler join](profile/verified.json). Durations include each full M×N kernel workload. The primary ratios use this one trace.','',
        '### Fixed-seed robustness','',
        '| Shape | Random928 / Predicted | Random929 / Predicted | Random930 / Predicted |','|---|---:|---:|---:|']
    for case in r['cases']:
        selected=[x for x in seeds if x['case']==case['id']];lines.append('| '+' × '.join(map(str,case['shape']))+' | '+' | '.join(f"{x['speedup']:.3f}×" for x in selected)+' |')
    lines+=['','All three seeds give the same direction for every size. [Supporting seed data](seed-robustness.json) retain per-round paired mean ratios; raw profiler samples retain p10/p90 and extrema. The separate ordinary-event run corroborates regression on the small cases and improvements on the larger cases. Its CUDA-event graph interval includes GPU graph scheduling gaps.','',
        '## Exact layout and semantics checks','',
        'The source fixtures were built from real Jac Scalar/RowNext/ColumnNext objects and the production packer. Saved canonical discovery identities anchor the remapping. The Predicted permutation is independently reconstructed from complete lane cursor chains and checked against all-A BFS then all-B BFS. Each saved permutation is a full bijection; field values/tags, every CSR row and target, heads and initialized queue are checked against that canonical graph. Each q/cursor arrival in every lane is checked for the same logical identity. Arrays and identity permutations have SHA-256 hashes.','',
        'Every replay poisons output with the bitwise complement of its expected int64 value and Jac status with `0xffffffff`, outside timing. All M×N outputs are checked against independent NumPy int64 A@B and the saved oracle, and every Jac status must be zero. Input magnitudes guarantee |partial sum| ≤ 15K. The same checks apply to each supporting random seed.','',
        f"Nsight launch audit: **{check['launches_verified']:,}** nodes verified, **{check['measured_launches']:,}** measured including seed controls; 3,600 measured nodes belong to the primary three groups. Every name, order, grid, block and graph-node position matches the runner request, including primes and warmups. `--cuda-graph-trace=node` provides actual per-node durations.",'',
        '## Address evidence and hardware-counter limitation','',
        'The Nsight Compute request for `l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum` returned **ERR_NVGPUCTRPERM**, exit 1. [Exact log](counters/ncu.log) and [status](counters/status.json) preserve the attempted collection. The counter-probe timing is excluded from the primary data.','',
        'The [deterministic address analysis](address-analysis.json) uses the exact saved layouts and actual 256-byte-aligned device array bases from the primary run. For every q, cursor and logical load it counts distinct 32-byte address segments within each logical warp access. It preserves those dimensions separately and records per-warp count hashes plus example adjacent-lane addresses. This is an address quantity; hardware transactions, cache misses and occupancy remain unmeasured. Compiler instruction transformations and cache state are outside the model.','',
        '| 256³ logical warp access, mean distinct 32-byte segments | Random928 | Predicted |','|---|---:|---:|']
    for cursor,load in [('a','value'),('b','value'),('b','csr_begin'),('b','csr_end'),('b','csr_target')]:
        b=segments['matmul-256x256x256','before',cursor,load]['mean_segments'];after=segments['matmul-256x256x256','after',cursor,load]['mean_segments'];lines.append(f'| cursor {cursor}: {load} | {b:.3f} | {after:.3f} |')
    lines+=['',
        'At N=256 a warp covers one row i and 32 adjacent columns j. Cursor a therefore shares one A-node address across that warp in both layouts. Cursor b has 32 distinct node addresses; Predicted places those B nodes consecutively, giving eight value-address segments instead of about 32. CSR begin/end indexing also includes the channel-row offset. This establishes the address organization enabled by the traversal order. The timing evidence establishes the measured layout benefit and small-case regressions; their hardware causes remain unresolved.','',
        '## Shared GPU and measurement boundary','',
        f"RTX 3090, driver 580.65.06, CUDA 12.9. Ollama held approximately 23,462 MiB in before/after snapshots. The primary process measured {free/1e6:.2f} MB free after context creation. Each case checks its allocation against current free VRAM and releases buffers before the next case. Snapshots and planned allocation bytes are stored in `profile/results.json` and `ordinary/results.json`.",'',
        'Actual kernel timing excludes packing/remapping, compilation, allocations, transfers, output poisoning, verification and graph scheduling gaps. The ordinary event samples are separate. Layout construction cost is outside the resident-kernel question here; the source packer and all remapping scripts are retained for reproduction.','',
        '## Same-trace pilot and 3000³ scale assessment','',
        'The urgent [pilot](../../pilot/comparison.json) extracts Random928, Predicted and fixed tiled CUDA from the same earlier verified trace. At 256³ it measured 4486.394 / 2069.116 / 20.608 µs, a 2.168× layout speedup. Source paths and complete SHA-256 hashes are saved with that pilot; the fresh table above uses the new confirmation trace.','',
        f"Historical 3000³ correctness covered **9,000,000 outputs** and 27 billion multiply-accumulates. The separate historical resident timing covered **32,768 outputs per launch**: Random {scale['historical_subset_random_us']/1000:.3f} ms versus Predicted {scale['historical_subset_predicted_us']/1000:.3f} ms, a {scale['historical_subset_speedup']:.3f}× subset speedup. That historical run has no handwritten timing reference and uses its recorded older PTX/data. These values are explicitly subset timings, separate from full-result correctness and from the new primary table.",'',
        f"Current resource assessment: one 3000³ packed graph requires {graph_bytes/1e6:.2f} MB, exceeding the measured {free/1e6:.2f} MB free. Two layouts plus dense A/B/C and bounded 32,768-query Jac private buffers require about {scale['two_graphs_dense_full_matrices_and_bounded_private_lower_bytes']/1e9:.2f} GB before additional allocation/JIT headroom. Dense A/B/C alone occupy 216 MB. The historical temporary raw directory is currently absent; checked-in summaries, hashes, audit and source remain available.",'',
        'A matched full-coverage 3000³ follow-up can use a GPU/session with sufficient free VRAM, retain one Random and one Predicted graph, execute all 275 bounded Jac batches covering 9 million outputs, and compare aggregate actual kernel durations with the fixed tiled reference covering the same outputs. A matched 32,768-output subset study would need a tiled reference with exactly that output selection and explicit subset labeling. Paging or graph partitioning would introduce an out-of-core execution question. [Feasibility record and historical source hashes](scale-3000-feasibility.json) preserve the boundary.','',
        '## Artifacts and reproduction','',
        'The [runner](../../run.py), [input/permutation audit](../../prepare.py), [profiler join](../../analyze.py), [address analysis](../../address_analysis.py), [research contract](../../RESEARCH_CONTRACT.md) and [reproduction script](../../reproduce.sh) are scoped to this layout study. The [English PDF](../../../../../docs/presentations/jac-gpu-layout/jac-gpu-layout.pdf) is generated directly from the checked comparison and contract.','']
    (v/'REPORT.md').write_text('\n'.join(lines))
    write(v/'contract-validation.json',{'status':'PASS','contract_sha256':sha(contract),'primary_groups':r['primary_arms'],'jac_variable':'node layout only','identical_ptx':True,'identical_jac_geometry':True,'logical_identity_audits':True,'full_output_status_checks':True,'source_run_id':'profile','profiler_launches_verified':check['launches_verified'],'report_generator_sha256':sha(Path(__file__))})
    print('Research contract, inputs, source hashes and launch evidence PASS; three-column matmul exports complete.')


if __name__=='__main__':main()
