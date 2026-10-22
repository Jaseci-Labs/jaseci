#!/usr/bin/env python3
"""Audit and remap the saved real production-packed Jac matmul graphs."""
import argparse
import hashlib
import json
import random
from pathlib import Path
import sys
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'handwritten_matmul'))
from benchmark import load,sha


def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def read(path):return json.loads(path.read_text())
def save(path,array):
    array=np.ascontiguousarray(array);path.write_bytes(array.tobytes())
    return {'file':path.name,'dtype':array.dtype.str,'shape':list(array.shape),'sha256':sha(path),'bytes':array.nbytes}
def get(directory,info):
    path=directory/info['file'];assert sha(path)==info['sha256'];return np.fromfile(path,dtype=info['dtype']).reshape(info['shape'])


def remap(base,order):
    values,tags,offsets,targets,heads,counts,initial,out,status,queue=base
    nodes=len(values);inverse=np.empty(nodes,dtype=np.int64);inverse[order]=np.arange(nodes)
    new_offsets=np.empty_like(offsets);parts=[];cursor=0
    for ch in range(2):
        rows=ch*(nodes+1)+order
        begin=offsets[rows];degree=offsets[rows+1]-begin
        assert np.all((degree>=0)&(degree<=1))
        new_offsets[ch*(nodes+1):(ch+1)*(nodes+1)]=np.r_[cursor,cursor+np.cumsum(degree)]
        part=inverse[targets[begin[degree==1]]];parts.append(part);cursor+=len(part)
    q=queue.copy();mask=q>=0;q[mask]=inverse[q[mask]]
    return [values[order],tags[order],new_offsets,np.concatenate(parts),inverse[heads],counts.copy(),initial.copy(),out.copy(),status.copy(),q]


def canonical_chains(base,shape):
    m,k,n=shape;lanes=m*n;nodes=len(base[0]);ai=base[4][:lanes].copy();bi=base[4][lanes:].copy();aa=[];bb=[]
    for q in range(k):
        np.testing.assert_array_equal(ai,np.repeat(ai[::n],n));np.testing.assert_array_equal(bi,np.tile(bi[:n],m))
        aa.append(ai[::n].copy());bb.append(bi[:n].copy())
        np.testing.assert_array_equal(base[0][ai],np.repeat((np.arange(m)+q)%7-3,n))
        np.testing.assert_array_equal(base[0][bi],np.tile((q*3+np.arange(n))%11-5,m))
        for cur,ch in [(ai,0),(bi,1)]:
            rows=ch*(nodes+1)+cur;begin=base[2][rows];end=base[2][rows+1]
            assert np.all(end-begin==(1 if q<k-1 else 0))
            cur[:]=base[3][begin] if q<k-1 else -1
    aa=np.stack(aa);bb=np.stack(bb);assert len(set(np.r_[aa.ravel(),bb.ravel()]))==nodes
    return aa,bb


def audit_layout(base,arrays,order,shape):
    assert np.array_equal(np.sort(order),np.arange(len(order)))
    expected=remap(base,order)
    for index in [0,1,2,3,4,5,6,9]:np.testing.assert_array_equal(arrays[index],expected[index])
    m,k,n=shape;nodes=len(order);lanes=m*n
    aa,bb=canonical_chains(base,shape);ai=arrays[4][:lanes].copy();bi=arrays[4][lanes:].copy()
    for q in range(k):
        np.testing.assert_array_equal(order[ai],np.repeat(aa[q],n));np.testing.assert_array_equal(order[bi],np.tile(bb[q],m))
        for cur,ch in [(ai,0),(bi,1)]:
            rows=ch*(nodes+1)+cur;begin=arrays[2][rows]
            cur[:]=arrays[3][begin] if q<k-1 else -1
    return {'all_node_fields_edges_heads_and_queue_remap_verified':True,'all_lane_cursor_arrivals_logically_identical':True,'rounds_per_cursor':k,'lanes':lanes}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=HERE.parent/'handwritten_matmul/validation/20261021/inputs/inputs.json');p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    source=read(a.source);ptx=a.source.parent/'Dot.ptx';assert sha(ptx)==source['ptx_sha256'];(a.output/'Dot.ptx').write_bytes(ptx.read_bytes())
    records=[]
    for case in source['cases']:
        old={x['label']:x for x in case['layouts']};directory=a.output/case['id'];directory.mkdir(exist_ok=True)
        base=[load(x,a.source.parent/case['id']) for x in old['Current']['files']]
        aa,bb=canonical_chains(base,case['shape']);expected_order=np.r_[aa.ravel(),bb.ravel()]
        layouts=[]
        for name,seed in [('after',None),('before',928),('random929',929),('random930',930)]:
            original=old['Predicted' if seed is None else 'Random-928'] if seed in [None,928] else None
            if original:
                arrays=[load(x,a.source.parent/case['id']) for x in original['files']];order=np.asarray(original['identity_order'],dtype=np.int64)
                assert hashlib.sha256(order.tobytes()).hexdigest()==original['identity_order_sha256']
            else:
                ids=list(range(len(base[0])));random.Random(seed).shuffle(ids);order=np.asarray(ids,dtype=np.int64);arrays=remap(base,order)
            if seed is None:np.testing.assert_array_equal(order,expected_order)
            audit=audit_layout(base,arrays,order,case['shape'])
            files=[save(directory/(name+f'-{i}.bin'),array) for i,array in enumerate(arrays)]
            layouts.append({'name':name,'seed':seed,'files':files,'identity_order':save(directory/(name+'-permutation.bin'),order),'audit':audit,'queue_capacity':old['Predicted']['queue_capacity'],'max_visits':old['Predicted']['max_visits']})
        expected=load(case['expected'],a.source.parent/case['id'])
        records.append({'id':case['id'],'shape':case['shape'],'nodes':case['nodes'],'lanes':case['walkers'],'expected':save(directory/'expected.bin',expected),'layouts':layouts,'predicted_strategy':'complete cursor-a BFS then complete cursor-b BFS; all A then all B','canonical_discovery_source':str(a.source),'source_current_hashes':[x['sha256'] for x in old['Current']['files']]})
        print(case['id'],'all permutations, graph remaps and lane traversals PASS',flush=True)
    write(a.output/'inputs.json',{'generator_sha256':sha(Path(__file__)),'source_manifest':str(a.source.relative_to(ROOT)) if a.source.is_absolute() else str(a.source),'source_manifest_sha256':sha(a.source),'source_jac_sha256':source['source_sha256'],'ptx_sha256':sha(a.output/'Dot.ptx'),'seeds':[928,929,930],'cases':records})


if __name__=='__main__':main()
