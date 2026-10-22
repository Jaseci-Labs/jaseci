#!/usr/bin/env python3
"""Bounded subtree extension: Random vs BFS with identical checked Jac PTX."""
import argparse
from collections import deque
import ctypes as c
import random
import statistics
import subprocess
from pathlib import Path
import numpy as np
from prepare import HERE,ROOT,read,write,save,get,sha
from run import snapshot
from benchmark import Driver
BEFORE='Jac before (Random928)';AFTER='Jac after (Predicted BFS)';REF='Handwritten checked CSR reference (after layout)'
FIELDS=['amount','alert','offsets','targets','heads','initial_count','initial_total','initial_has_alert','initial_visited','initial_threshold']
CASES=['ragged37-mixed33','binary4095-mixed256','binary4095-leaf1024','irregular16383-mixed256','chain2048-mixed32']


def permute(data,order):
    amount,alert,offsets,targets,heads,*states=data;n=len(amount);inverse=np.empty(n,dtype=np.int64);inverse[order]=np.arange(n)
    degrees=offsets[order+1]-offsets[order];off=np.r_[0,np.cumsum(degrees)]
    old_targets=np.concatenate([targets[offsets[node]:offsets[node+1]] for node in order]);new_targets=inverse[old_targets]
    new_heads=np.full_like(heads,-1);mask=heads>=0;new_heads[mask]=inverse[heads[mask]]
    result=[amount[order],alert[order],off,new_targets,new_heads,*[x.copy() for x in states]]
    np.testing.assert_array_equal(order[new_targets],old_targets)
    np.testing.assert_array_equal(order[new_heads[mask]],heads[mask])
    for old,new in zip(data[5:],result[5:]):np.testing.assert_array_equal(old,new)
    return result


def oracle(data):
    amount,alert,off,targets,heads,*states=data;out=[]
    for lane,head in enumerate(heads):
        count,total,flag,visited,threshold=[int(x[lane]) for x in states];todo=deque([] if head==-1 else [int(head)])
        while todo:
            nd=todo.popleft();visited+=1
            if amount[nd]>=threshold:count+=1;total+=int(amount[nd]);flag|=int(alert[nd])
            todo.extend(int(x) for x in targets[off[nd]:off[nd+1]])
        out.append([count,total,flag,visited,threshold])
    return np.asarray(out,dtype=np.int64)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=HERE.parent/'subtree_query/validation/20261021/inputs.json');p.add_argument('--output',type=Path,required=True);p.add_argument('--warmup',type=int,default=3);p.add_argument('--repeats',type=int,default=15);p.add_argument('--inner',type=int,default=8);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    old=read(a.source);assert old['jac_source_sha256']==sha(ROOT/'jac/examples/gpu/subtree_query.jac')
    production_ptx=a.source.parent/'codegen/original.ptx';cuda_source=HERE.parent/'subtree_query/subtree.cu';cuda_ptx=a.output/'subtree.ptx'
    cmd=['/usr/local/cuda-12.9/bin/nvcc','-ptx','-O3','-arch=compute_86','-std=c++17',str(cuda_source),'-o',str(cuda_ptx)];subprocess.run(cmd,check=True)
    result={'runner_sha256':sha(Path(__file__)),'source_manifest_sha256':sha(a.source),'contract_sha256':sha(HERE/'RESEARCH_CONTRACT.md'),
        'jac_ptx_sha256':sha(production_ptx),'jac_source_sha256':old['jac_source_sha256'],'jac_function_loaded_once_for_both_layouts':True,
        'after_strategy':'ordered multi-source BFS, seeded in original query-lane order, first occurrence; original CSR neighbor order',
        'reference_layout':'after','reference_kernel':'subtree_checked','reference_source_sha256':sha(cuda_source),'reference_ptx_sha256':sha(cuda_ptx),'nvcc_command':cmd,
        'primary_arms':[BEFORE,AFTER,REF],'warmup':a.warmup,'repeats':a.repeats,'inner':a.inner,'order_seed':237,'gpu_before':snapshot(),'cases':[],'records':[]}
    d=Driver();result['gpu']=d.name;result['memory_before']=d.memory()
    try:
        jac=d.kernel(production_ptx,'jac_SubtreeQuery_csr_batch');ref=d.kernel(cuda_ptx,'subtree_checked')
        for index,case in enumerate([c for c in old['cases'] if c['id'] in CASES]):
            directory=a.source.parent/'inputs'/case['id']
            def original(name):
                info=case['files'][name];path=directory/info['path'];assert sha(path)==info['sha256'];return np.fromfile(path,dtype=info['dtype']).reshape(info['shape'])
            data=[original(name) for name in FIELDS];expected=original('expected');np.testing.assert_array_equal(original('serial'),expected)
            n=len(data[0]);todo=deque();seen=set();bfs=[]
            for head in data[4]:
                if head>=0 and int(head) not in seen:seen.add(int(head));todo.append(int(head))
            while todo:
                nd=todo.popleft();bfs.append(nd)
                for target in data[3][data[2][nd]:data[2][nd+1]]:
                    if int(target) not in seen:seen.add(int(target));todo.append(int(target))
            assert len(bfs)==n
            random_order=list(range(n));random.Random(928).shuffle(random_order)
            orders={'before':np.asarray(random_order,dtype=np.int64),'after':np.asarray(bfs,dtype=np.int64)}
            layouts={name:permute(data,order) for name,order in orders.items()}
            saved=a.output/'inputs'/case['id'];saved.mkdir(parents=True,exist_ok=True)
            input_meta={}
            for name,arrays in layouts.items():
                np.testing.assert_array_equal(oracle(arrays),expected)
                input_meta[name]={'permutation':save(saved/(name+'-permutation.bin'),orders[name]),'arrays':[save(saved/(name+f'-{i}.bin'),array) for i,array in enumerate(arrays)]}
            expected_meta=save(saved/'expected.bin',expected)
            q=case['queries'];cap=case['queue_capacity'];planned=sum(x.nbytes for arrays in layouts.values() for x in arrays)+3*q*(cap*8+44);assert planned<d.memory()['free']*.55
            readonly={name:[d.upload(x) for x in arrays] for name,arrays in layouts.items()};graphs={};outputs={};statuses={};launches={}
            grid=((q+127)//128,1,1);block=(128,1,1)
            for name,label,fn,kernel in [('before',BEFORE,jac,'jac_SubtreeQuery_csr_batch'),('after',AFTER,jac,'jac_SubtreeQuery_csr_batch'),('after',REF,ref,'subtree_checked')]:
                out=[d.upload(np.full(q,-999,dtype=np.int64)) for _ in range(5)];status=d.upload(np.full(q,0xffffffff,dtype=np.uint32));queue=d.upload(np.full(q*cap,-1,dtype=np.int64))
                args=[*readonly[name],*out,status,queue,n,case['edges'],q,cap,case['max_visits']];holders=[c.c_uint64(v) for v in args]
                graphs[label]=d.capture(fn,grid,block,holders,a.inner);outputs[label]=out;statuses[label]=status;launches[label]={'kernel':kernel,'grid':grid,'block':block}
            poisons=[np.ascontiguousarray(np.bitwise_not(expected[:,j])) for j in range(5)];bad=np.full(q,0xffffffff,dtype=np.uint32)
            for phase,rounds in [('warmup',a.warmup),('measured',a.repeats)]:
                for pair in range(rounds):
                    order=list(graphs);random.Random(237+100*index+pair+(10000 if phase=='measured' else 0)).shuffle(order)
                    for label in order:
                        for ptr,poison in zip(outputs[label],poisons):d.call('cuMemcpyHtoD_v2',ptr,poison.ctypes.data,poison.nbytes)
                        d.call('cuMemcpyHtoD_v2',statuses[label],bad.ctypes.data,bad.nbytes)
                        us=d.measure(graphs[label],a.inner)
                        actual=np.column_stack([d.download(ptr,q,np.int64) for ptr in outputs[label]])
                        np.testing.assert_array_equal(actual,expected);np.testing.assert_array_equal(d.download(statuses[label],q,np.uint32),np.zeros(q,dtype=np.uint32))
                        result['records'].append({'case':case['id'],'arm':label,'phase':phase,'pair':pair,'event_us':us,'all_outputs_and_statuses_checked':True})
            meta={'id':case['id'],'tree_nodes':case['tree_nodes'],'packed_nodes':n,'queries':q,'inputs':input_meta,'expected':expected_meta,'same_logical_node_identities_edges_query_mapping_verified':True,'serial_and_cpu_oracles_verified':True,'full_output_status_checks':True,'queue_capacity':cap,'max_visits':case['max_visits'],'planned_device_bytes':planned,'arms':{}}
            for label,launch in launches.items():
                samples=[x['event_us'] for x in result['records'] if x['case']==case['id'] and x['arm']==label and x['phase']=='measured'];meta['arms'][label]={**launch,'median_event_us':statistics.median(samples)}
            result['cases'].append(meta);d.clear_case();write(a.output/'results.json',result);print(case['id'],{name:round(info['median_event_us'],3) for name,info in meta['arms'].items()},flush=True)
        result['complete']=True;result['memory_after']=d.memory()
    finally:d.close();result['gpu_after']=snapshot();write(a.output/'results.json',result)


if __name__=='__main__':main()
