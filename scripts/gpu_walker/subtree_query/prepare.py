#!/usr/bin/env python3
"""Build real Jac trees, production CSR, dual CPU oracles and LLVM ablations."""
import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import random
import re
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
from common import HERE, ROOT, read, save_array, sha, write
sys.path.insert(0, str(HERE.parent))
from compare_layouts import memory_context


def cpu_query(children, amounts, alerts, root, threshold):
    pending = deque([] if root is None else [root])
    count = total = visited = 0
    has_alert = False
    peak = len(pending)
    while pending:
        current = pending.popleft()
        visited += 1
        if amounts[current] >= threshold:
            count += 1
            total += amounts[current]
            has_alert |= alerts[current]
        pending.extend(children[current])
        peak = max(peak, len(pending))
    return [count, total, int(has_alert), visited, threshold], peak


def tree(n, branch, seed):
    rng = random.Random(seed)
    children = [[] for _ in range(n)]
    depths = [0] * n
    available = [0]
    for node in range(1, n):
        if branch == 'irregular':
            # Random bounded-degree parents, with occasional deeper continuations.
            parent = node-1 if node % 7 == 0 and len(children[node-1]) < 5 else rng.choice(available)
        else:
            parent = (node-1)//int(branch)
        children[parent].append(node)
        depths[node] = depths[parent]+1
        if branch == 'irregular':
            if len(children[parent]) == 5:
                available.remove(parent)
            available.append(node)
    amounts = [rng.randrange(-1000, 1001) for _ in range(n)]
    alerts = [rng.random() < .17 for _ in range(n)]
    return children, amounts, alerts, depths


# Bounded full workloads; query count and subtree sizes are explicit factors.
CASES = [
    ('ragged37-mixed33', 37, 2, 33, 'mixed', 'varied'),
    ('binary511-root32', 511, 2, 32, 'root', 'varied'),
    ('binary511-mixed256', 511, 2, 256, 'mixed', 'varied'),
    ('binary4095-root16', 4095, 2, 16, 'root', 'varied'),
    ('binary4095-mixed256', 4095, 2, 256, 'mixed', 'varied'),
    ('binary4095-leaf1024', 4095, 2, 1024, 'leaf', 'varied'),
    ('binary4095-small1024', 4095, 2, 1024, 'small', 'varied'),
    ('ternary3280-root16', 3280, 3, 16, 'root', 'varied'),
    ('quaternary4093-mixed128', 4093, 4, 128, 'mixed', 'varied'),
    ('chain2048-mixed32', 2048, 1, 32, 'mixed', 'varied'),
    ('irregular4095-mixed128', 4095, 'irregular', 128, 'mixed', 'varied'),
    ('irregular16383-mixed256', 16383, 'irregular', 256, 'mixed', 'varied'),
    ('binary1023-root1', 1023, 2, 1, 'root', 'varied'),
    ('binary1023-root32', 1023, 2, 32, 'root', 'varied'),
    ('binary1023-root128', 1023, 2, 128, 'root', 'varied'),
    ('binary1023-root128-all', 1023, 2, 128, 'root', 'all'),
    ('binary1023-root128-none', 1023, 2, 128, 'root', 'none'),
]


def emit_codegen(schema, spec, directory):
    from jaclang.compiler.backends.native.ptx import ptx_target
    from jaclang.compiler.backends.native.ptx_csr import build_csr_module
    from jaclang.compiler.backends.native.llvm import binding as llvm
    directory.mkdir(exist_ok=True)
    target = ptx_target()
    module = build_csr_module([spec], target)
    raw = str(module)
    (directory/'input.ll').write_text(raw)
    assert target.emit_assembly(module) == schema.ptx
    result = {'generator_sha256': sha(Path(__file__)), 'input_ir_sha256': sha(directory/'input.ll'),
              'kernel': schema.kernel_name, 'fields': schema.field_paths(), 'state': schema.state_paths(),
              'parameters': spec, 'variants': {}}
    # The spec is represented by exact CSR metadata in the provenance file.
    from jaclang.compiler.backends.native.ptx_csr import csr_metadata
    result['parameters'] = csr_metadata(spec)['parameters']
    for label, codes in [('original', []), ('sroa', []), ('O2', []),
                         ('O2_no_overflow', ['integer.overflow']),
                         ('O2_no_validation', ['invalid.node', 'visit.limit.exceeded', 'invalid.csr.offsets', 'queue.capacity.exceeded']),
                         ('O2_unchecked', ['integer.overflow', 'invalid.node', 'visit.limit.exceeded', 'invalid.csr.offsets', 'queue.capacity.exceeded'])]:
        changes = []
        def bypass(match):
            a, b = match.groups()
            if a in codes or b in codes:
                assert not (a in codes and b in codes)
                changes.append(a if a in codes else b)
                return '  br label %' + (b if a in codes else a)
            return match.group()
        text = re.sub(r'(?m)^\s*br i1 [^\n]+, label %([\w.]+), label %([\w.]+)$', bypass, raw)
        mod = llvm.parse_assembly(text)
        mod.verify()
        pb = llvm.create_pass_builder(target, llvm.create_pipeline_tuning_options(speed_level=2))
        if label.startswith('O2'):
            pb.getModulePassManager().run(mod, pb)
        elif label == 'sroa':
            pm = llvm.ModulePassManager(); pm.add_sroa_pass(); pm.run(mod, pb)
        mod.verify()
        (directory/(label+'.ll')).write_text(str(mod))
        ptx = target.emit_assembly(mod)
        (directory/(label+'.ptx')).write_text(ptx)
        command = ['/usr/local/cuda-12.9/bin/ptxas','-arch=sm_86','-v',str(directory/(label+'.ptx')),'-o',str(directory/(label+'.cubin'))]
        log = subprocess.run(command, capture_output=True, text=True, check=True)
        (directory/(label+'-ptxas.log')).write_text(log.stdout+log.stderr)
        result['variants'][label] = {'ptx_sha256': sha(directory/(label+'.ptx')),
            'allocas': text.count(' alloca '), 'optimized_allocas': str(mod).count(' alloca '),
            'local_load_sites': ptx.count('ld.local.'), 'local_store_sites': ptx.count('st.local.'),
            'global_load_sites': ptx.count('ld.global.'), 'global_store_sites': ptx.count('st.global.'),
            'bypassed_error_branches': changes, 'ptxas_command': command, 'ptxas_log': log.stdout+log.stderr}
    assert result['variants']['original']['ptx_sha256'] == hashlib.sha256(schema.ptx.encode()).hexdigest()
    write(directory/'codegen.json', result)
    print('Codegen:', json_summary(result), flush=True)


def json_summary(result):
    return {label: (info['allocas'],info['local_load_sites'],info['local_store_sites']) for label,info in result['variants'].items()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--memory-probe', type=Path, required=True)
    p.add_argument('--codegen-only', action='store_true')
    a = p.parse_args(); a.output.mkdir(parents=True, exist_ok=True)
    from jaclang.runtime import gpu
    from jaclang.runtime.runtime import JacRuntime
    from jaclang.compiler.backends.native.ptx import compile_ptx_frontend
    from jaclang.compiler.backends.native.ptx_walker import select_chain_walkers
    from jaclang.compiler.backends.native.llvm import binding as llvm
    llvm.initialize_all_targets(); llvm.initialize_all_asmprinters()
    source = ROOT/'jac/examples/gpu/subtree_query.jac'
    probe = read(a.memory_probe)
    memory_budget = int(probe['memory_after_context']['free']*.55)
    with memory_context():
        model = JacRuntime.jac_import(target='subtree_query', base_path=str(source.parent))[0]
        schema = gpu.walker_schema(model.SubtreeQuery, 'csr')
        spec = select_chain_walkers(compile_ptx_frontend(str(source)), ['SubtreeQuery'])[0]
        assert schema.field_paths() == ['amount','alert'], schema.field_paths()
        assert schema.state_paths() == ['count','total','has_alert','visited','threshold'], schema.state_paths()
        emit_codegen(schema, spec, a.output/'codegen')
        if a.codegen_only:
            return
        records = []
        for name, n, branch, queries, mode, predicate in CASES:
            begin = time.perf_counter()
            # Same tree and root choices across query-batch and selectivity controls.
            children, amounts, alerts, depths = tree(n, branch, 928+n)
            rng = random.Random(237+n)
            leaves = [i for i,row in enumerate(children) if not row]
            small = [i for i in range(n) if depths[i] >= max(depths)-1]
            roots = ([0]*queries if mode == 'root' else
                     [rng.choice(leaves if mode == 'leaf' else small if mode == 'small' else range(n)) for _ in range(queries)])
            if mode == 'mixed':
                roots[0] = 0
                if name == 'ragged37-mixed33':
                    roots[-1] = None
            thresholds = [(-1001 if predicate == 'all' else 1001 if predicate == 'none' else [-1001,-500,0,250,1001][i%5]) for i in range(queries)]
            oracle_peaks = [cpu_query(children, amounts, alerts, root, threshold) for root,threshold in zip(roots,thresholds)]
            expected = [x[0] for x in oracle_peaks]
            capacity = max(1,max(x[1] for x in oracle_peaks))
            max_visits = max(1,max(x[3] for x in expected))
            # Six-arm ablation peak: shared immutable arrays; private outputs/status/queues.
            graph_upper = (4*n+1)*8
            per_arm = capacity*queries*8 + queries*(5*8+4)
            bytes_upper = graph_upper+queries*(6*8)+8*per_arm
            assert bytes_upper < memory_budget, (name, bytes_upper, memory_budget)
            oracle_ms = (time.perf_counter()-begin)*1000
            begin = time.perf_counter()
            nodes = [model.Item(amount=amount, alert=alert) for amount,alert in zip(amounts,alerts)]
            for parent,row in enumerate(children):
                for child in row:
                    JacRuntime.connect(nodes[parent], nodes[child], model.Child)
            graph_ms = (time.perf_counter()-begin)*1000
            starts = [None if root is None else nodes[root] for root in roots]
            serial = []
            begin = time.perf_counter()
            for start,threshold in zip(starts,thresholds):
                walker = model.SubtreeQuery(threshold=threshold)
                if start is not None:
                    JacRuntime.spawn(walker, start)
                serial.append([int(getattr(walker,path)) for path in schema.state_paths()])
            assert serial == expected, name
            serial_ms = (time.perf_counter()-begin)*1000
            begin = time.perf_counter()
            packed = gpu.pack_walkers(schema, [model.SubtreeQuery(threshold=t) for t in thresholds], starts, capacity, max_visits)
            pack_ms = (time.perf_counter()-begin)*1000
            buffers = packed.buffers
            identity = {id(node): i for i,node in enumerate(nodes)}
            original_ids = [identity[id(node)] for node in packed.nodes]
            remap = {old: new for new,old in enumerate(original_ids)}
            assert list(buffers.values) == [amounts[i] for i in original_ids]
            assert list(buffers.extra_values[0]) == [int(alerts[i]) for i in original_ids]
            for new,old in enumerate(original_ids):
                actual = list(buffers.targets[buffers.offsets[new]:buffers.offsets[new+1]])
                assert actual == [remap[child] for child in children[old]], (name, old)
            assert list(buffers.heads) == [-1 if r is None else remap[r] for r in roots]
            directory = a.output/'inputs'/name; directory.mkdir(parents=True,exist_ok=True)
            all_arrays = dict(zip(['amount','alert','offsets','targets','heads','initial_count','initial_total','initial_has_alert','initial_visited','initial_threshold'],buffers.arrays()[:10]))
            all_arrays.update(expected=expected,serial=serial,original_node_ids=original_ids,original_roots=[-1 if r is None else r for r in roots])
            files = {key: save_array(directory,key,data) for key,data in all_arrays.items()}
            visits = [row[3] for row in expected]
            counts = [row[0] for row in expected]
            record = {'id':name,'tree_nodes':n,'packed_nodes':len(packed.nodes),'edges':len(buffers.targets),
                'branching':branch,'max_depth':max(depths),'queries':queries,'root_mode':mode,'predicate_mode':predicate,
                'queue_capacity':capacity,'max_visits':max_visits,'queue_bytes_per_arm':capacity*queries*8,
                'allocation_upper_eight_arms':bytes_upper,'memory_budget':memory_budget,'layout':'production pack_walkers discovery order',
                'total_node_visits':sum(visits),'total_matches':sum(counts),'visit_min':min(visits),'visit_median':float(np.median(visits)),'visit_max':max(visits),
                'max_abs_amount':max(map(abs,amounts)),'sum_bound':max(map(abs,amounts))*max_visits,
                'setup_ms':{'cpu_oracle':oracle_ms,'graph_objects':graph_ms,'serial_jac':serial_ms,'packing':pack_ms},
                'serial_and_independent_oracle_verified':True,'packed_graph_identity_verified':True,'files':files}
            records.append(record)
            print(name,'visits',sum(visits),'queue',capacity,'queries',queries,'serial_ms',round(serial_ms,2),flush=True)
        manifest = {'timestamp_utc':datetime.now(timezone.utc).isoformat(),'generator_sha256':sha(Path(__file__)),
            'jac_source':str(source.relative_to(ROOT)),'jac_source_sha256':sha(source),'memory_probe':probe,
            'semantics':'FIFO traversal includes root; match amount>=threshold; count,total,has_alert among matches; visited over all arrivals; threshold retained',
            'fields':schema.field_paths(),'states':schema.state_paths(),'cases':records}
        write(a.output/'inputs.json',manifest)


if __name__ == '__main__':
    main()
