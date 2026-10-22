#!/usr/bin/env python3
"""Verify source evidence and export the three-way subtree report and datasets."""
import argparse
import csv
import os
from pathlib import Path
import re
import numpy as np
from common import HERE, ROOT, load_array, read, sha, write

GROUPS=[('original','Jac original'),('optimized','Jac O2'),('handwritten','CUDA checked')]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('validation',type=Path);a=p.parse_args();v=a.validation
    manifest=read(v/'inputs.json');codegen=read(v/'codegen/codegen.json');correct=read(v/'correctness.json')
    ordinary=read(v/'ordinary/results.json');profile=read(v/'profile/results.json');verified=read(v/'profile/verified.json')
    ablation=read(v/'ablation-profile/verified.json');ab_run=read(v/'ablation-profile/results.json');ab_event=read(v/'ablation-ordinary/results.json')
    assert correct['status']=='PASS' and correct['gpu_launches_checked']==68
    assert manifest['generator_sha256']==sha(HERE/'prepare.py')
    assert codegen['generator_sha256']==sha(HERE/'prepare.py')
    assert codegen['input_ir_sha256']==sha(v/'codegen/input.ll')
    assert manifest['jac_source_sha256']==sha(ROOT/manifest['jac_source'])
    assert correct['validator_sha256']==sha(HERE/'validate.py')
    for run,checked in [('profile',verified),('ablation-profile',ablation)]:
        assert checked['status']=='PASS' and checked['analyzer_sha256']==sha(HERE/'analyze.py')
        assert checked['results_sha256']==sha(v/run/'results.json') and checked['sqlite_sha256']==sha(v/run/'trace.sqlite')
    for run in [ordinary,profile,ab_run,ab_event]:
        assert run['complete'] and run['input_sha256']==sha(v/'inputs.json')
        assert run['runner_sha256']==sha(HERE/'run.py') and run['common_sha256']==sha(HERE/'common.py')
        assert run['cuda_source_sha256']==sha(HERE/'subtree.cu')
        assert run['reused_driver_sha256']==sha(HERE.parent/'handwritten_matmul/benchmark.py')
        assert all(x['all_query_fields_and_status_verified'] for x in run['cases'])
        for arm,info in run['variants'].items():
            if arm.startswith('Jac'):
                label={'Jac original':'original','Jac O2':'O2'}.get(arm,arm.removeprefix('Jac '))
                assert info['ptx_sha256']==codegen['variants'][label]['ptx_sha256']
    assert profile['variants']['CUDA checked']['ptx_sha256']==ordinary['variants']['CUDA checked']['ptx_sha256']
    assert correct['variants']['CUDA checked']['ptx_sha256']==profile['variants']['CUDA checked']['ptx_sha256']
    for label,info in codegen['variants'].items():assert info['ptx_sha256']==sha(v/'codegen'/(label+'.ptx'))
    for case in manifest['cases']:
        assert case['serial_and_independent_oracle_verified'] and case['packed_graph_identity_verified']
        for info in case['files'].values():load_array(v/'inputs'/case['id'],info)
    # Control identity is checked against raw files, not workload labels.
    cases={c['id']:c for c in manifest['cases']}
    control_ids=['binary1023-root1','binary1023-root128-all','binary1023-root128-none','binary1023-root128']
    for name in control_ids:
        for field in ['amount','alert','offsets','targets']:
            assert cases[name]['files'][field]['sha256']==cases[control_ids[0]]['files'][field]['sha256']
    one=cases[control_ids[0]];many=cases[control_ids[1]]
    expected_one=load_array(v/'inputs'/one['id'],one['files']['expected'])
    expected_many=load_array(v/'inputs'/many['id'],many['files']['expected'])
    np.testing.assert_array_equal(expected_many,np.repeat(expected_one,128,axis=0))
    for name in control_ids:
        head=load_array(v/'inputs'/name,cases[name]['files']['heads']);assert np.all(head==0)
    lookup={(x['case'],x['arm']):x for x in verified['summaries']}
    aux={(x['case'],x['arm']):x for x in ablation['summaries']}
    event={(c['id'],arm):x for c in ordinary['cases'] for arm,x in c['arms'].items()}
    source_paths=['inputs.json','profile/results.json','profile/verified.json','profile/trace.sqlite','profile/trace.nsys-rep','ordinary/results.json','codegen/codegen.json','correctness.json']
    sources={path:sha(v/path) for path in source_paths}
    primary=v/'primary';primary.mkdir(exist_ok=True)
    rows=[]
    for case in manifest['cases']:
        row={key:case[key] for key in ['id','tree_nodes','packed_nodes','queries','max_depth','queue_capacity','total_node_visits','visit_min','visit_max']}
        row.update({key+'_us':lookup[(case['id'],arm)]['median_us'] for key,arm in GROUPS})
        rows.append(row)
    write(primary/'comparison.json',{'unit':'microseconds','statistic':'median actual GPU kernel end-start','source_run_id':'profile',
        'fixed_layout':'production pack_walkers discovery order; identical saved arrays for all three groups',
        'groups':{'original':'production CSR LLVM and existing target-machine code generation',
                  'optimized':'same raw LLVM plus checked standard LLVM O2 middle-end; experimental path',
                  'handwritten':'fixed checked per-query CUDA CSR FIFO kernel, same graph and predicates'},
        'sources_sha256':sources,'rows':rows})
    with (primary/'comparison.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=[*rows[0],'unit','source_run_id'],lineterminator='\n');writer.writeheader()
        for row in rows:writer.writerow({**row,'unit':'microseconds','source_run_id':'profile'})
    for key,arm in GROUPS:
        write(primary/(key+'.json'),{'group':key,'arm':arm,'unit':'microseconds','source_run_id':'profile','sources_sha256':sources,
            'summaries':[lookup[(c['id'],arm)] for c in manifest['cases']],
            'measured_kernel_samples':[x for x in verified['samples'] if x['arm']==arm and x['phase']=='measured'],
            'ordinary_event_samples':[x for x in ordinary['records'] if x['arm']==arm]})
    reproduce_link=os.path.relpath(HERE/'reproduce.sh',v)
    pdf_link=os.path.relpath(ROOT/'docs/presentations/jac-gpu-subtree/jac-gpu-subtree.pdf',v)
    deck_link=os.path.relpath(ROOT/'docs/presentations/jac-gpu-subtree/generate.py',v)
    total_visits=sum(c['total_node_visits'] for c in manifest['cases'])
    o2ratios=[row['optimized_us']/row['original_us'] for row in rows]
    cudratios=[row['handwritten_us']/row['original_us'] for row in rows]
    sample_n=profile['inner']*profile['repeats']
    f=lambda value:f'{value:,.3f}'
    lines=['# Batched subtree query on Jac GPU','',
        'Original production Jac CSR and the fixed checked handwritten per-query CSR kernel have similar timings across this sweep. The experimental checked LLVM O2 path is usually slower. This backend already uses phi nodes for its state and has zero allocas/local stack storage. The measured result differs from the earlier named-cursor matmul promotion result.','',
        '## Query and implementations','',
        'Each independent query starts at its root, includes that root, and visits every descendant in FIFO order. A node qualifies when `amount >= threshold`. The query returns the qualifying count, signed int64 amount sum, OR of alerts on qualifying nodes, total visited count and retained threshold. Queries share a read-only tree and maintain private state and queues.','',
        'The three primary groups use exactly the same saved production-packed CSR arrays, roots, thresholds, queue capacity and 128-thread per-query lane mapping. Immutable GPU pointers are shared across arms; outputs, status and FIFO scratch are private.','',
        '- **Original Jac:** the existing single-cursor CSR lowering and target-machine code generation settings.',
        '- **Checked optimized Jac:** the identical raw LLVM module, standard LLVM O2 middle-end, verification and the same target emission. The experimental path preserves all production checks and status handling.',
        '- **Handwritten CUDA:** one thread per query, the same CSR edge traversal and predicates, slot-major circular FIFO (`queue[slot * queries + lane]`), bounded visits/queue and checked int64 updates. The same kernel is used for every workload.','',
        '## Primary three-way comparison','',
        f'Median resident **actual GPU kernel duration**, microseconds. All cells come from the single interleaved randomized `profile` run, with {profile["warmup"]} warmup and {profile["repeats"]} measured rounds, {profile["inner"]} sequential CUDA graph nodes per replay, and {sample_n} measured kernel samples per cell. Seed {profile["seed"]}. Nsight uses `--cuda-graph-trace=node`; its end−start intervals measure each actual kernel.','',
        '| Workload | Queries | Original Jac | Checked Jac + O2 | Handwritten CUDA |','|---|---:|---:|---:|---:|']
    for row in rows:lines.append(f"| {row['id']} | {row['queries']} | {f(row['original_us'])} | {f(row['optimized_us'])} | {f(row['handwritten_us'])} |")
    lines += ['',f'Across the 17 cases, handwritten/original median-time ratios range from {min(cudratios):.3f}× to {max(cudratios):.3f}×; checked O2/original ranges from {min(o2ratios):.3f}× to {max(o2ratios):.3f}×. Lower time is faster. The 16,383-node irregular mixed batch takes 8.271 ms original Jac, 8.939 ms checked O2 and 8.365 ms handwritten in this run.','',
        '[CSV](primary/comparison.csv) · [compact JSON with source identifiers and hashes](primary/comparison.json) · [original dataset](primary/original.json) · [checked O2 dataset](primary/optimized.json) · [handwritten dataset](primary/handwritten.json). Individual durations, p10/p90, extrema, per-round means and ordinary-event samples are preserved in the datasets and raw results.','',
        '## Measured explanation','',
        '### The CSR backend already carries state in SSA','',
        'Inspection starts from `ptx_csr.lower_csr`, independently of the named-cursor backend. FIFO read/write positions, pending/step counters and the five query states are LLVM phi values. Original CSR has zero allocas; SROA-only emits byte-identical PTX. Original and O2 both have zero PTX local loads/stores and zero stack/spill bytes in ptxas. Actual driver-JIT attributes confirm zero local bytes; original uses 38 registers, O2 40 and checked handwritten 40.','',
        'O2 changes control flow and static instruction sites (global stores 13→8; global loads remain 12) while retaining all checks. Its elapsed-time result is usually a slowdown here. Static site counts and register counts describe generated code; the hardware mechanism behind this timing difference remains unresolved.','',
        '### Full traversal, batch size and predicate work','',
        'The general FIFO algorithms visit every subtree node even when the predicate rejects all nodes. The exact full workload is checked, including visited count. A mixed batch can contain one full-root traversal plus many short subtree queries; the query visit distribution is recorded below. Across heterogeneous batches, both total visits and per-query lengths change, so they are reported together.','',
        f'The controlled 1-query versus 128-query all-match contrast uses byte-identical graph arrays, root 0, threshold −1001 and identical per-query results. Original Jac takes {f(lookup[(one["id"],"Jac original")]["median_us"])} versus {f(lookup[(many["id"],"Jac original")]["median_us"])} µs: 128× as many node visits in {lookup[(many["id"],"Jac original")]["median_us"]/lookup[(one["id"],"Jac original")]["median_us"]:.2f}× the latency. This measures the batched execution benefit for this graph and kernel.','',
        'All-match and no-match 128-query controls also reuse byte-identical graph arrays and roots. Both visit 130,944 nodes. Original Jac takes '+f(lookup[('binary1023-root128-all','Jac original')]['median_us'])+' versus '+f(lookup[('binary1023-root128-none','Jac original')]['median_us'])+' µs; checked O2 takes '+f(lookup[('binary1023-root128-all','Jac O2')]['median_us'])+' versus '+f(lookup[('binary1023-root128-none','Jac O2')]['median_us'])+' µs. The predicate changes count/sum/alert work while traversal volume stays fixed.','',
        '### Check and FIFO-layout ablations','',
        'A separate interleaved eight-arm trace holds each workload fixed. LLVM diagnostic variants bypass overflow, graph/limit checks, or both before O2. Their contract is the validated finite tree inputs, zero initial accumulators, exact sufficient queue/visit bounds and proven int64 sums. Checked kernels additionally handle the invalid-input/error fixtures. CUDA unchecked uses the same restricted benchmark inputs.','',
        'CUDA query-major retains the full checks and traversal while changing scratch addressing to `queue[lane * capacity + slot]`. This changes address generation and physical scratch layout together.','',
        '| Supplementary workload | Checked O2 | O2 no overflow | O2 no validation | O2 unchecked | CUDA checked | CUDA unchecked | CUDA query-major |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    aux_arms=['Jac O2','Jac O2_no_overflow','Jac O2_no_validation','Jac O2_unchecked','CUDA checked','CUDA unchecked','CUDA query-major']
    for name in ['binary4095-mixed256','irregular16383-mixed256','binary1023-root1','binary1023-root128-all','binary1023-root128-none']:
        lines.append('| '+name+' | '+' | '.join(f(aux[(name,arm)]['median_us']) for arm in aux_arms)+' |')
    lines += ['',
        'Removing selected checks speeds these whole generated implementations on the listed inputs. The variants are optimized independently, so the differences describe each experiment’s combined generated-code effect. Per-check additive cost percentages remain unresolved.','',
        'Query-major scratch is faster for the two listed mixed-subtree workloads and slower for the uniform 128-query full-root workloads. The ordinary-event ablation run corroborates these directions. Hardware attribution to cache, coalescing, occupancy and memory transactions remains open; this evidence consists of timing traces, source-controlled transformations and static/driver codegen attributes.','',
        '## Workloads and VRAM planning','',
        f'All {total_visits:,} query-node visits in the 17 complete workloads are checked against both serial Jac and an independent queue-based Python oracle. Trees include balanced binary/ternary trees, ragged binary/quaternary trees, a 2,048-node chain, and irregular bounded-degree trees. Amounts span −1000…1000; thresholds include all-match, partial-match and no-match cases. Leaves and short subtrees exercise varied query lengths.','',
        '| Workload | Tree / packed nodes | Depth | Query visits min / median / max | FIFO capacity | FIFO bytes per arm |','|---|---:|---:|---:|---:|---:|']
    for case in manifest['cases']:
        lines.append(f"| {case['id']} | {case['tree_nodes']} / {case['packed_nodes']} | {case['max_depth']} | {case['visit_min']} / {case['visit_median']:g} / {case['visit_max']} | {case['queue_capacity']} | {case['queue_bytes_per_arm']:,} |")
    peak=max(c['planned_device_bytes'] for c in ab_run['cases']);free=manifest['memory_probe']['memory_after_context']['free'];budget=manifest['cases'][0]['memory_budget']
    lines += ['',
        f'The memory probe measured {free/1e6:.2f} MB free after context creation. Preparation budgets {budget/1e6:.2f} MB (55% of that value); each run rechecks current free VRAM before allocation. Exact peak live FIFO occupancy is computed over every query. Scratch is `queries × exact capacity × 8` bytes per arm. The eight-arm run’s largest planned live allocation is {peak/1e6:.2f} MB. Read-only inputs are shared and cases are released sequentially.','',
        '## Correctness and launch audit','',
        '- Production Jac Item/Child objects and `gpu.pack_walkers` produce the actual CSR, with its discovery layout held fixed across the three arms. Saved node identities, field columns, each CSR row/target and query heads are checked against the original object tree. All saved arrays have SHA-256 checksums.',
        '- Serial Jac runs every query; an independent CPU reference computes all five state fields. The replay runner independently traverses the saved packed CSR and checks those oracle outputs again.',
        '- Every replay poisons all five output columns and status outside timing, then verifies every query field and zero status after execution. The maximum absolute sum is bounded by `max_abs_amount × max_visits`, safely inside signed int64.',
        f'- Direct status testing passes {len(correct["cases"])} fixtures × 4 checked kernels = {correct["gpu_launches_checked"]} standalone GPU launches, comparing original Jac, checked O2, checked CUDA and checked query-major CUDA against the unmodified production host LLVM JIT. Cases cover ragged/negative queries, private initial state, equality above 2^53, positive and negative sum overflow, count and visited overflow, malformed heads/targets/CSR, queue/visit limits, a cycle, and empty roots. Failing lanes preserve every poisoned result field.',
        f'- Primary Nsight join: {verified["launches_verified"]:,} launches verified, {verified["measured_launches"]:,} measured. Supplementary join: {ablation["launches_verified"]:,} verified, {ablation["measured_launches"]:,} measured. Every kernel name, chronological position, grid and block matches the exact runner request, including prime and warmup nodes.',
        '- The existing subtree CPU/JIT suite passes all four tests. Raw status evidence is in [correctness.json](correctness.json); raw traces and joins are in `profile/` and `ablation-profile/`.','',
        '## Measurement boundary and shared environment','',
        'RTX 3090, driver 580.65.06, CUDA 12.9 nvcc/ptxas, bundled Jac LLVM NVPTX. The GPU is shared with Ollama, which holds approximately 23,462 MiB in the saved snapshots. Before/after snapshots and free-memory values are stored per run. Absolute timings reflect that shared context; the primary ratios use the same interleaved run.','',
        'The primary metric is actual GPU kernel end−start. The ordinary event runs measure CUDA graph replay time per invocation, including graph scheduling gaps. Allocations, module compilation, graph preparation, transfers, poisoning and verification occur outside both timing intervals. `inputs.json` records CPU oracle, graph construction, serial Jac and packing time. Runner case records separately save allocation, H2D and graph capture/prime time; each replay’s D2H/verification is outside its event interval.','',
        '## Reproduction and presentation','',
        f'Run [reproduce.sh]({reproduce_link}) from the repository root with a fresh output directory and GPU access. The pipeline rebuilds real graphs, emits variants, validates, profiles and exports the report. [commands.txt](commands.txt) records the completed run commands; [provenance.json](provenance.json) records source hashes.','',
        f'The [English PDF deck]({pdf_link}) and [deck generator]({deck_link}) use white backgrounds and sans-serif typography, and verify the measured source hashes when generated.','']
    (v/'REPORT.md').write_text('\n'.join(lines))
    # Preserve all secondary arms and all 17 cases in a compact machine-readable appendix.
    write(v/'ablation-summary.json',{'unit':'microseconds','source_run_id':'ablation-profile','summaries':ablation['summaries'],
        'contract':'LLVM/CUDA unchecked variants use validated finite bounded tree inputs; query-major CUDA retains full checked semantics',
        'source_sha256':{path:sha(v/path) for path in ['ablation-profile/results.json','ablation-profile/verified.json','ablation-profile/trace.sqlite','ablation-ordinary/results.json']}})
    print('All source/input hashes verified; report and three primary datasets exported.')


if __name__=='__main__':main()
