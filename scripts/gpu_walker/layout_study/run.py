#!/usr/bin/env python3
"""Layout-only Jac matmul pair plus fixed tiled CUDA reference, interleaved."""
import argparse
import ctypes as c
from datetime import datetime,timezone
from pathlib import Path
import random
import statistics
import subprocess
import sys
import numpy as np
from prepare import HERE,ROOT,read,write,get,sha,remap,audit_layout
sys.path.insert(0,str(HERE.parent/'handwritten_matmul'))
from benchmark import Driver
BEFORE='Jac before (Random928 + checked LLVM O2)'
AFTER='Jac after (Predicted + checked LLVM O2)'
REFERENCE='Handwritten CUDA reference (nvcc O3)'
LABELS={'before':BEFORE,'after':AFTER,'reference':REFERENCE,'random929':'Random929 robustness','random930':'Random930 robustness'}


def snapshot():return subprocess.check_output(['nvidia-smi'],text=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--jac-ptx',type=Path,required=True);p.add_argument('--warmup',type=int,default=5);p.add_argument('--repeats',type=int,default=25);p.add_argument('--inner',type=int,default=16);p.add_argument('--order-seed',type=int,default=237)
    p.add_argument('--case-id');p.add_argument('--only-arm',choices=list(LABELS));a=p.parse_args();assert a.warmup>=0 and min(a.repeats,a.inner)>0
    a.output.mkdir(parents=True,exist_ok=True);source=read(a.inputs)
    ptx=a.jac_ptx;codegen=read(ptx.parent/'codegen.json')
    assert codegen['production_ptx_sha256']==source['ptx_sha256']
    assert codegen['optimized_ptx_sha256']==sha(ptx) and codegen['pipeline']=='standard LLVM O2; checked semantics retained'
    assert source['source_jac_sha256']==sha(ROOT/'jac/examples/gpu/named_cursors.jac')
    cuda_source=HERE.parent/'handwritten_matmul/matmul.cu';cuda_ptx=a.output/'matmul.ptx'
    cmd=['/usr/local/cuda-12.9/bin/nvcc','-ptx','-O3','-arch=compute_86','-std=c++17',str(cuda_source),'-o',str(cuda_ptx)]
    subprocess.run(cmd,check=True)
    ids=['before','after','reference','random929','random930'] if not a.only_arm else [a.only_arm]
    result={'runner_sha256':sha(Path(__file__)),'prepare_sha256':sha(HERE/'prepare.py'),'driver_sha256':sha(HERE.parent/'handwritten_matmul/benchmark.py'),
        'contract_sha256':sha(HERE/'RESEARCH_CONTRACT.md'),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'input_manifest_sha256':sha(a.inputs),
        'jac_compilation_policy':'checked standard LLVM O2','optimized_codegen_sha256':sha(ptx.parent/'codegen.json'),'jac_ptx_sha256':sha(ptx),'jac_kernel':'jac_Dot_cursors_batch','jac_function_loaded_once_for_all_layouts':True,
        'reference_kernel':'matmul_tiled_i64','reference_source_sha256':sha(cuda_source),'reference_ptx_sha256':sha(cuda_ptx),'nvcc_command':cmd,
        'primary_arms':[BEFORE,AFTER,REFERENCE],'warmup':a.warmup,'repeats':a.repeats,'inner':a.inner,'order_seed':a.order_seed,
        'event_metric':'CUDA-event graph replay / inner, including graph scheduling gaps','gpu_before':snapshot(),'cases':[],'records':[]}
    d=Driver();result['gpu']=d.name;result['memory_before']=d.memory()
    try:
        jac=d.kernel(ptx,result['jac_kernel']);tiled=d.kernel(cuda_ptx,'matmul_tiled_i64')
        cases=[x for x in source['cases'] if not a.case_id or x['id']==a.case_id];assert cases
        for case_index,case in enumerate(cases):
            m,k,n=case['shape'];lanes=m*n;directory=a.inputs.parent/case['id'];layouts={x['name']:x for x in case['layouts']}
            arrays={name:[get(directory,info) for info in layout['files']] for name,layout in layouts.items()}
            orders={name:get(directory,layout['identity_order']) for name,layout in layouts.items()}
            base=remap(arrays['after'],np.argsort(orders['after']))
            for name in layouts:audit_layout(base,arrays[name],orders[name],case['shape'])
            A=np.fromfunction(lambda i,q:(i+q)%7-3,(m,k),dtype=np.int64).astype(np.int64)
            B=np.fromfunction(lambda q,j:(q*3+j)%11-5,(k,n),dtype=np.int64).astype(np.int64)
            expected=A@B;np.testing.assert_array_equal(expected.ravel(),get(directory,case['expected']))
            assert 15*k<np.iinfo(np.int64).max
            planned=sum(sum(x.nbytes for x in arrays[name]) for name in ids if name!='reference')+(A.nbytes+B.nbytes+expected.nbytes if 'reference' in ids else 0)
            free=d.memory()['free'];assert planned<int(free*.55),(planned,free)
            graphs={};outs={};statuses={};launches={};addresses={}
            for name in ids:
                label=LABELS[name]
                if name=='reference':
                    data=[A,B,np.full((m,n),-999,dtype=np.int64)];params=[c.c_int(m),c.c_int(k),c.c_int(n)]
                    fn=tiled;grid=((n+15)//16,(m+15)//16,1);block=(16,16,1);kernel='matmul_tiled_i64'
                else:
                    info=layouts[name];data=[x.copy() for x in arrays[name]]
                    data[7]=np.full(lanes,-999,dtype=np.int64);data[8]=np.full(lanes,0xffffffff,dtype=np.uint32)
                    assert np.all(data[5]==1) and np.all(data[6]==0)
                    params=[c.c_uint64(v) for v in [case['nodes'],len(data[3]),lanes,info['queue_capacity'],info['max_visits']]]
                    fn=jac;grid=((lanes+127)//128,1,1);block=(128,1,1);kernel='jac_Dot_cursors_batch'
                pointers=[d.upload(x) for x in data]
                assert all(pointer%256==0 for pointer in pointers)
                holders=[c.c_uint64(v) for v in pointers]+params
                graphs[label]=d.capture(fn,grid,block,holders,a.inner)
                outs[label]=pointers[2] if name=='reference' else pointers[7]
                if name!='reference':
                    statuses[label]=pointers[8]
                    addresses[name]={'values':pointers[0],'tags':pointers[1],'offsets':pointers[2],'targets':pointers[3]}
                launches[label]={'kernel':kernel,'grid':grid,'block':block}
            poison=np.ascontiguousarray(np.bitwise_not(expected));bad=np.full(lanes,0xffffffff,dtype=np.uint32)
            for phase,rounds in [('warmup',a.warmup),('measured',a.repeats)]:
                for pair in range(rounds):
                    order=list(graphs);random.Random(a.order_seed+case_index*100+pair+(10000 if phase=='measured' else 0)).shuffle(order)
                    for label in order:
                        d.call('cuMemcpyHtoD_v2',outs[label],poison.ctypes.data,poison.nbytes)
                        if label in statuses:d.call('cuMemcpyHtoD_v2',statuses[label],bad.ctypes.data,bad.nbytes)
                        us=d.measure(graphs[label],a.inner)
                        np.testing.assert_array_equal(d.download(outs[label],(m,n),np.int64),expected)
                        if label in statuses:np.testing.assert_array_equal(d.download(statuses[label],lanes,np.uint32),np.zeros(lanes,dtype=np.uint32))
                        result['records'].append({'case':case['id'],'arm':label,'phase':phase,'pair':pair,'event_us':us,'all_outputs_and_statuses_checked':True})
            meta={'id':case['id'],'shape':case['shape'],'lanes':lanes,'expected_sha256':case['expected']['sha256'],'planned_device_bytes':planned,'free_before_case':free,
                'all_node_permutations_and_logical_traversals_verified':True,'all_outputs_and_statuses_verified':True,'device_array_bases':addresses,'arms':{}}
            for label,launch in launches.items():
                values=[x['event_us'] for x in result['records'] if x['case']==case['id'] and x['arm']==label and x['phase']=='measured']
                meta['arms'][label]={**launch,'median_event_us':statistics.median(values),'min_event_us':min(values),'max_event_us':max(values),'sample_n':len(values)}
            result['cases'].append(meta);d.clear_case();write(a.output/'results.json',result)
            print(case['id'],{name:round(info['median_event_us'],3) for name,info in meta['arms'].items()},flush=True)
        result['complete']=True;result['memory_after']=d.memory()
    finally:
        d.close();result['gpu_after']=snapshot();write(a.output/'results.json',result)


if __name__=='__main__':main()
