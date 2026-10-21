#!/usr/bin/env python3
"""Compare checked PTX variants with production LLVM JIT on error/status paths.

Uses real Jac objects and the production packer; mutations intentionally create
invalid device inputs after packing. No production source is modified.
"""
import argparse
import ctypes as c
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from benchmark import Driver, sha
from compare_named_layouts import schemas_and_modules


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codegen', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    from jaclang.runtime import gpu_cursors as multi
    from jaclang.runtime.runtime import JacRuntime
    schemas, modules = schemas_and_modules({'Dot'})
    schema = schemas['Dot']
    mod = next(module for module in modules.values() if hasattr(module, 'Dot'))
    spec = schema.cursor_spec
    assert hashlib.sha256(schema.ptx.encode()).hexdigest() == sha(args.codegen / 'baseline.ptx')

    def fixture(av=(2, 3), bv=(4, 5), *, initial=0, capacity=2, limit=20, cycle=False, branch=False):
        aa = [mod.Scalar(value=int(v)) for v in av]
        bb = [mod.Scalar(value=int(v)) for v in bv]
        for nodes, edge in ((aa, mod.RowNext), (bb, mod.ColumnNext)):
            for a, b in zip(nodes, nodes[1:]):
                JacRuntime.connect(a, b, edge)
            if cycle:
                JacRuntime.connect(nodes[-1], nodes[0], edge)
        if branch:
            JacRuntime.connect(aa[0], mod.Scalar(value=9), mod.RowNext)
        return multi.pack_cursors(schema, [mod.Dot(total=initial)],
                                  [dict(a=aa[0], b=bb[0])], capacity, limit,
                                  prediction_budget=20).buffers

    cases = []
    def add(name, buffers, code):
        cases.append((name, buffers, code))
    add('valid', fixture(), 0)
    add('multiply_overflow', fixture((2**62,), (3,)), 3)
    add('add_overflow', fixture((1,), (1,), initial=2**63-1), 3)
    add('round_limit_cycle', fixture((1,), (1,), cycle=True, limit=5), 2)
    add('queue_capacity_branch', fixture(capacity=1, branch=True), 6)
    x = fixture(); x.heads[0] = -1; add('invalid_negative_head', x, 1)
    x = fixture(); x.heads[0] = len(x.tags); add('invalid_large_head', x, 1)
    x = fixture(); x.targets[x.offsets[x.heads[0]]] = len(x.tags); add('invalid_edge_target', x, 1)
    x = fixture(); x.offsets[x.heads[0]] = -1; add('invalid_negative_csr', x, 5)
    x = fixture(); x.offsets[x.heads[0]+1] = len(x.targets)+1; add('invalid_csr_end', x, 5)
    x = fixture(); x.seed_counts[0] = x.queue_capacity+1; add('seed_queue_capacity', x, 6)
    x = fixture(); x.tags[x.heads[0]] = 0; add('type_mismatch_skips_visit', x, 0)
    x = fixture(); x.seed_counts[0] = 0; add('empty_channel', x, 0)

    d = Driver()
    labels = ['baseline', 'O2', 'hoist_sroa']
    kernels = {label: d.kernel(args.codegen / (label+'.ptx'), schema.kernel_name) for label in labels}
    d.lib.cuFuncGetAttribute.argtypes = [c.POINTER(c.c_int), c.c_int, c.c_void_p]
    d.lib.cuFuncGetAttribute.restype = c.c_int
    attributes = {}
    for label, fn in kernels.items():
        attributes[label] = {}
        for name, key in [('local_bytes_per_thread', 3), ('registers_per_thread', 4),
                          ('ptx_version', 5), ('binary_version', 6)]:
            value = c.c_int()
            d.call('cuFuncGetAttribute', c.byref(value), key, fn)
            attributes[label][name] = value.value
    result = {'validator_sha256': sha(Path(__file__)), 'gpu': d.name,
              'actual_driver_jit_function_attributes': attributes,
              'ptx_sha256': {label: sha(args.codegen / (label+'.ptx')) for label in labels},
              'oracle': 'Unmodified production LLVM host JIT; exact outputs and status, poisoned before each GPU launch',
              'cases': []}
    try:
        for name, buffers, code in cases:
            buffers.results[0] = -998877665544
            buffers.status[0] = 0xffffffff
            arrays = [np.asarray(a).copy() for a in buffers.arrays()]
            vals, status = multi.run_jit(spec, buffers)
            assert status == [code], (name, status, code)
            if code:
                assert vals[0] == [-998877665544], (name, vals)
            entry = {'case': name, 'expected_status': status, 'expected_results': vals[0], 'variants': {}}
            for label, fn in kernels.items():
                pointers = [d.upload(a) for a in arrays]
                holders = [c.c_uint64(v) for v in pointers + buffers.arguments()]
                params = (c.c_void_p*len(holders))(*(c.addressof(v) for v in holders))
                d.call('cuLaunchKernel', fn, 1, 1, 1, 128, 1, 1, 0, d.stream, params, None)
                d.call('cuStreamSynchronize', d.stream)
                actual = d.download(pointers[7], 1, np.int64).tolist()
                actual_status = d.download(pointers[8], 1, np.uint32).tolist()
                assert actual == vals[0], (name, label, actual, vals)
                assert actual_status == status, (name, label, actual_status, status)
                entry['variants'][label] = {'status': actual_status, 'results': actual, 'pass': True}
                d.clear_case()
            result['cases'].append(entry)
    finally:
        d.close()
    result['status'] = 'PASS'
    result['gpu_launches_checked'] = len(cases)*len(labels)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
