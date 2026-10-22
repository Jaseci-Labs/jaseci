#!/usr/bin/env python3
"""Check CPU-JIT/GPU outputs and status paths for both Jac variants and CUDA."""
import argparse
import ctypes as c
from pathlib import Path
import sys
import numpy as np
from common import HERE, ROOT, Driver, attributes, read, sha, write
sys.path.insert(0,str(HERE.parent))
from compare_layouts import memory_context


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--validation',type=Path,required=True)
    a=p.parse_args();folder=a.validation
    from jaclang.runtime.runtime import JacRuntime
    from jaclang.runtime import gpu
    from jaclang.compiler.backends.native.ptx import compile_ptx_frontend
    from jaclang.compiler.backends.native.ptx_walker import select_chain_walkers
    from jaclang.compiler.backends.native.ptx_csr import build_csr_module
    from jaclang.compiler.backends.native.llvm import binding as llvm
    llvm.initialize_all_targets();llvm.initialize_all_asmprinters()
    with memory_context():
        source=ROOT/'jac/examples/gpu/subtree_query.jac'
        model=JacRuntime.jac_import(target='subtree_query',base_path=str(source.parent))[0]
        schema=gpu.walker_schema(model.SubtreeQuery,'csr')
        spec=select_chain_walkers(compile_ptx_frontend(str(source)),['SubtreeQuery'])[0]
        target=llvm.Target.from_default_triple().create_target_machine(opt=2)
        module=build_csr_module([spec],target,device=False)
        engine=llvm.create_mcjit_compiler(module,target);engine.finalize_object()
        pointer_types=[c.POINTER(c.c_int64)]*15+[c.POINTER(c.c_uint32),c.POINTER(c.c_int64)]
        oracle=c.CFUNCTYPE(None,*pointer_types,*[c.c_uint64]*6)(engine.get_function_address('jac_SubtreeQuery_csr_lane'))
        def fixture(amounts=(2,-4,7),alerts=(False,True,True),edges=((0,1),(0,2)),roots=(0,),thresholds=(0,),capacity=2,limit=10,initial=None):
            nodes=[model.Item(amount=int(x),alert=bool(y)) for x,y in zip(amounts,alerts)]
            for i,j in edges:JacRuntime.connect(nodes[i],nodes[j],model.Child)
            walkers=[model.SubtreeQuery(threshold=int(t),**(initial or {})) for t in thresholds]
            return gpu.pack_walkers(schema,walkers,[None if r is None else nodes[r] for r in roots],capacity,limit).buffers
        cases=[]
        def add(name,x,codes):cases.append((name,x,codes))
        add('valid_ragged_negative_thresholds',fixture(roots=(0,1,2,None),thresholds=(-4,-4,8,-100)),[0]*4)
        add('valid_private_initial_state',fixture(initial={'count':4,'total':9,'has_alert':True,'visited':2}),[0])
        add('exact_int64_above_2pow53',fixture(amounts=(2**53+1,),alerts=(False,),edges=(),thresholds=(2**53+1,),capacity=1),[0])
        add('total_positive_overflow',fixture(initial={'total':2**63-1}),[3])
        add('total_negative_overflow',fixture(amounts=(-4,),alerts=(True,),edges=(),thresholds=(-4,),initial={'total':-2**63+3}),[3])
        add('count_overflow',fixture(initial={'count':2**63-1}),[3])
        add('visited_overflow_nonmatch',fixture(thresholds=(1001,),initial={'visited':2**63-1}),[3])
        x=fixture();x.heads[0]=-2;add('negative_head',x,[1])
        x=fixture();x.heads[0]=len(x.values);add('out_of_range_head',x,[1])
        x=fixture();x.targets[0]=len(x.values);add('out_of_range_target',x,[1])
        x=fixture();x.offsets[0]=-1;add('negative_csr_begin',x,[5])
        x=fixture();x.offsets[1]=len(x.targets)+1;add('large_csr_end',x,[5])
        add('queue_full',fixture(capacity=1),[6])
        add('visit_limit',fixture(limit=1),[2])
        add('cycle_limit',fixture(amounts=(1,),alerts=(False,),edges=((0,0),),capacity=1,limit=3),[2])
        x=fixture();x.queue_capacity=0;add('zero_capacity_nonempty',x,[6])
        x=fixture(roots=(None,));x.queue_capacity=0;add('zero_capacity_empty',x,[0])
        d=Driver()
        variant_paths={'Jac original':(folder/'codegen/original.ptx',schema.kernel_name),
                       'Jac O2':(folder/'codegen/O2.ptx',schema.kernel_name),
                       'CUDA checked':(folder/'ordinary/subtree.ptx','subtree_checked'),
                       'CUDA query-major':(folder/'ordinary/subtree.ptx','subtree_query_major')}
        functions={name:d.kernel(path,kernel) for name,(path,kernel) in variant_paths.items()}
        report={'status':'RUNNING','validator_sha256':sha(Path(__file__)),'gpu':d.name,
                'oracle':'unmodified production CSR host LLVM control flow, direct JIT execution',
                'variants':{name:{'ptx_sha256':sha(variant_paths[name][0]),'attributes':attributes(d,fn)} for name,fn in functions.items()},'cases':[]}
        try:
            for name,buffers,codes in cases:
                m=len(buffers.heads)
                arrays=[np.asarray(x).copy() for x in buffers.arrays()]
                for x in arrays[10:15]:x[:]=-998877665544
                arrays[15][:]=0xffffffff
                queue=np.full(max(1,m*buffers.queue_capacity),-1,dtype=np.int64)
                saved=[x.copy() for x in arrays]+[queue.copy()]
                scalar=[len(buffers.values),len(buffers.targets),m,buffers.queue_capacity,buffers.max_visits]
                pointers=[c.cast(x.ctypes.data,typ) for x,typ in zip([*arrays,queue],pointer_types)]
                for lane in range(m):oracle(*pointers,*scalar,lane)
                expected=np.column_stack(arrays[10:15]);expected_status=arrays[15]
                assert expected_status.tolist()==codes,(name,expected_status,codes)
                for lane,code in enumerate(codes):
                    if code:assert np.all(expected[lane]==-998877665544)
                entry={'case':name,'expected':expected.tolist(),'expected_status':codes,'variants':{}}
                for label,fn in functions.items():
                    device=[d.upload(x) for x in saved]
                    holders=[c.c_uint64(v) for v in [*device,*scalar]]
                    params=(c.c_void_p*len(holders))(*(c.addressof(v) for v in holders))
                    d.call('cuLaunchKernel',fn,(m+127)//128,1,1,128,1,1,0,d.stream,params,None)
                    d.call('cuStreamSynchronize',d.stream)
                    actual=np.column_stack([d.download(ptr,m,np.int64) for ptr in device[10:15]])
                    actual_status=d.download(device[15],m,np.uint32)
                    np.testing.assert_array_equal(actual,expected,err_msg=name+' '+label)
                    np.testing.assert_array_equal(actual_status,expected_status,err_msg=name+' '+label)
                    entry['variants'][label]={'pass':True,'outputs':actual.tolist(),'status':actual_status.tolist()}
                    d.clear_case()
                report['cases'].append(entry)
            report['status']='PASS';report['gpu_launches_checked']=len(cases)*len(functions)
        finally:
            d.close();write(folder/'correctness.json',report)
        print(report['status'],len(cases),'fixtures',report['gpu_launches_checked'],'GPU launches')


if __name__=='__main__':main()
