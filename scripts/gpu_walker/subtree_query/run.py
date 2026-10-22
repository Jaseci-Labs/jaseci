#!/usr/bin/env python3
"""Interleaved resident subtree CSR benchmark with complete replay verification."""
import argparse
import ctypes as c
from datetime import datetime, timezone
import random
import statistics
import subprocess
import time
from pathlib import Path
import numpy as np
from common import HERE, Driver, attributes, load_array, read, sha, snapshot, write

PRIMARY = [('Jac original','original','jac_SubtreeQuery_csr_batch'),
           ('Jac O2','O2','jac_SubtreeQuery_csr_batch'),
           ('CUDA checked','cuda','subtree_checked')]
SUPPLEMENTARY = [('Jac O2_no_overflow','O2_no_overflow','jac_SubtreeQuery_csr_batch'),
                 ('Jac O2_no_validation','O2_no_validation','jac_SubtreeQuery_csr_batch'),
                 ('Jac O2_unchecked','O2_unchecked','jac_SubtreeQuery_csr_batch'),
                 ('CUDA unchecked','cuda','subtree_unchecked'),
                 ('CUDA query-major','cuda','subtree_query_major')]
INPUT_NAMES = ['amount','alert','offsets','targets','heads','initial_count','initial_total','initial_has_alert','initial_visited','initial_threshold']


def replay_oracle(arrays):
    amount, alert, offsets, targets, heads = arrays[:5]
    from collections import deque
    results = []
    for lane,root in enumerate(heads):
        count,total,flag,visited,threshold = [int(x[lane]) for x in arrays[5:10]]
        todo = deque([] if root == -1 else [int(root)])
        while todo:
            nd = todo.popleft(); visited += 1
            if amount[nd] >= threshold:
                count += 1; total += int(amount[nd]); flag |= int(alert[nd])
            todo.extend(int(v) for v in targets[offsets[nd]:offsets[nd+1]])
        results.append([count,total,flag,visited,threshold])
    return np.asarray(results,dtype=np.int64)


def upload(driver, array, setup):
    array = np.ascontiguousarray(array)
    ptr = c.c_uint64()
    begin = time.perf_counter()
    driver.call('cuMemAlloc_v2',c.byref(ptr),max(array.nbytes,8))
    setup['allocate_ms'] += (time.perf_counter()-begin)*1000
    driver.allocs.append(ptr.value)
    begin = time.perf_counter()
    if array.nbytes:
        driver.call('cuMemcpyHtoD_v2',ptr,array.ctypes.data,array.nbytes)
    setup['H2D_ms'] += (time.perf_counter()-begin)*1000
    return ptr.value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--ablations',action='store_true')
    p.add_argument('--warmup',type=int,default=5)
    p.add_argument('--repeats',type=int,default=25)
    p.add_argument('--inner',type=int,default=8)
    p.add_argument('--seed',type=int,default=928)
    a = p.parse_args()
    assert a.warmup >= 0 and min(a.repeats,a.inner) > 0
    a.output.mkdir(parents=True,exist_ok=True)
    source = read(a.inputs)
    codegen = a.inputs.parent/'codegen'
    cuda = a.output/'subtree.ptx'
    command = ['/usr/local/cuda-12.9/bin/nvcc','-ptx','-O3','-arch=compute_86','-std=c++17',str(HERE/'subtree.cu'),'-o',str(cuda)]
    begin = time.perf_counter();subprocess.run(command,check=True);compile_ms=(time.perf_counter()-begin)*1000
    arms = PRIMARY+(SUPPLEMENTARY if a.ablations else [])
    result = {'runner_sha256':sha(Path(__file__)),'common_sha256':sha(HERE/'common.py'),
        'reused_driver_sha256':sha(HERE.parent/'handwritten_matmul/benchmark.py'),
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'input_sha256':sha(a.inputs),
        'input_manifest':str(a.inputs.resolve()),'warmup':a.warmup,'repeats':a.repeats,'inner':a.inner,'seed':a.seed,
        'event_metric':'CUDA-event graph replay duration / inner, including GPU graph scheduling gaps',
        'gpu_before':snapshot(),'cuda_source_sha256':sha(HERE/'subtree.cu'),'nvcc_command':command,'nvcc_compile_ms':compile_ms,
        'variants':{},'cases':[],'records':[],'primary_arms':[x[0] for x in PRIMARY]}
    d = Driver(); result['gpu']=d.name; result['memory_before']=d.memory()
    try:
        functions = {}
        for label,variant,name in arms:
            path = cuda if variant == 'cuda' else codegen/(variant+'.ptx')
            fn = d.kernel(path,name); functions[label]=fn
            result['variants'][label]={'kernel':name,'ptx_path':str(path),'ptx_sha256':sha(path),'driver_attributes':attributes(d,fn)}
        for index,case in enumerate(source['cases']):
            case_begin = time.perf_counter()
            directory = a.inputs.parent/'inputs'/case['id']
            arrays = [load_array(directory,case['files'][name]) for name in INPUT_NAMES]
            expected = load_array(directory,case['files']['expected'])
            serial = load_array(directory,case['files']['serial'])
            np.testing.assert_array_equal(serial,expected)
            np.testing.assert_array_equal(replay_oracle(arrays),expected)
            verify_ms = (time.perf_counter()-case_begin)*1000
            queries = case['queries']; capacity = case['queue_capacity']
            assert case['sum_bound'] < np.iinfo(np.int64).max
            readonly_bytes = sum(x.nbytes for x in arrays)
            arm_bytes = queries*(5*8+4)+max(8,capacity*queries*8)
            planned = readonly_bytes+len(arms)*arm_bytes
            free = d.memory()['free']
            assert planned <= min(int(free*.55),case['memory_budget']), (case['id'],planned,free)
            setup = {'allocate_ms':0.,'H2D_ms':0.,'capture_prime_ms':0.,'saved_input_oracle_ms':verify_ms}
            pointers = [upload(d,x,setup) for x in arrays]
            exes = {};outputs={};statuses={}
            grid,block = ((queries+127)//128,1,1),(128,1,1)
            for label,variant,name in arms:
                out = [upload(d,np.full(queries,-999,dtype=np.int64),setup) for _ in range(5)]
                status = upload(d,np.full(queries,0xffffffff,dtype=np.uint32),setup)
                scratch = upload(d,np.full(queries*capacity,-1,dtype=np.int64),setup)
                scalars = [case['packed_nodes'],case['edges'],queries,capacity,case['max_visits']]
                holders = [c.c_uint64(v) for v in [*pointers,*out,status,scratch,*scalars]]
                begin = time.perf_counter()
                exes[label] = d.capture(functions[label],grid,block,holders,a.inner)
                setup['capture_prime_ms'] += (time.perf_counter()-begin)*1000
                outputs[label]=out; statuses[label]=status
            poisons = [np.ascontiguousarray(np.bitwise_not(expected[:,j])) for j in range(5)]
            bad_status = np.full(queries,0xffffffff,dtype=np.uint32)
            for phase,rounds in [('warmup',a.warmup),('measured',a.repeats)]:
                for pair in range(rounds):
                    order = [x[0] for x in arms]
                    random.Random(a.seed+index*100+pair+(10000 if phase == 'measured' else 0)).shuffle(order)
                    for label in order:
                        for pointer,poison in zip(outputs[label],poisons):
                            d.call('cuMemcpyHtoD_v2',pointer,poison.ctypes.data,poison.nbytes)
                        d.call('cuMemcpyHtoD_v2',statuses[label],bad_status.ctypes.data,bad_status.nbytes)
                        us = d.measure(exes[label],a.inner)
                        actual = np.column_stack([d.download(pointer,queries,np.int64) for pointer in outputs[label]])
                        np.testing.assert_array_equal(actual,expected,err_msg=case['id']+' '+label)
                        np.testing.assert_array_equal(d.download(statuses[label],queries,np.uint32),np.zeros(queries,dtype=np.uint32))
                        result['records'].append({'case':case['id'],'arm':label,'phase':phase,'pair':pair,'event_us':us,'all_query_fields_and_status_checked':True})
            meta = {key:case[key] for key in ['id','tree_nodes','packed_nodes','edges','queries','branching','max_depth','root_mode','predicate_mode','queue_capacity','max_visits','total_node_visits','total_matches','visit_min','visit_median','visit_max']}
            meta.update(planned_device_bytes=planned,free_before_case=free,allocation=setup,
                memory_with_case=d.memory(),all_query_fields_and_status_verified=True,arms={})
            for label,variant,name in arms:
                values=[x['event_us'] for x in result['records'] if x['case']==case['id'] and x['arm']==label and x['phase']=='measured']
                meta['arms'][label]={'kernel':name,'grid':grid,'block':block,'median_event_us':statistics.median(values),'min_event_us':min(values),'max_event_us':max(values),'samples':len(values)}
            result['cases'].append(meta);d.clear_case()
            write(a.output/'results.json',result)
            print(case['id'],{label:round(info['median_event_us'],3) for label,info in meta['arms'].items()},flush=True)
        result['memory_after']=d.memory(); result['complete']=True
    finally:
        d.close();result['gpu_after']=snapshot();write(a.output/'results.json',result)


if __name__ == '__main__':
    main()
