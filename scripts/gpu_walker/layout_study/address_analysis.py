#!/usr/bin/env python3
"""Deterministic logical address segments, separated by q, cursor and warp load."""
import argparse
import hashlib
from pathlib import Path
import numpy as np
from prepare import read,write,get,sha


def summarize(addresses):
    sentinel=np.iinfo(np.uint64).max
    padded=np.full(((len(addresses)+31)//32)*32,sentinel,dtype=np.uint64);padded[:len(addresses)]=addresses
    words=np.sort(padded.reshape(-1,32),axis=1)
    valid=words!=sentinel
    unique=(valid[:,0].astype(np.int64)+np.sum((words[:,1:]!=words[:,:-1])&valid[:,1:],axis=1))
    segments=np.where(valid,words//32,sentinel)
    counts=valid[:,0].astype(np.int64)+np.sum((segments[:,1:]!=segments[:,:-1])&valid[:,1:],axis=1)
    return {'warp_events':len(counts),'mean_segments':float(np.mean(counts)),'median_segments':float(np.median(counts)),
        'min_segments':int(np.min(counts)),'max_segments':int(np.max(counts)),'sum_segments':int(np.sum(counts)),
        'mean_unique_addresses':float(np.mean(unique)),'per_warp_segment_counts_sha256':hashlib.sha256(counts.astype('<i8').tobytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--profile',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    source=read(a.inputs);profile=read(a.profile);assert profile['input_manifest_sha256']==sha(a.inputs)
    profcases={x['id']:x for x in profile['cases']};records=[];summaries=[]
    for case in source['cases']:
        m,k,n=case['shape'];lanes=m*n;nodes=case['nodes'];directory=a.inputs.parent/case['id']
        for layout in case['layouts']:
            name=layout['name']
            if name not in ['before','after']:continue
            arrays=[get(directory,f) for f in layout['files']];values,tags,offsets,targets,heads=arrays[:5]
            bases=profcases[case['id']]['device_array_bases'][name];assert all(b%256==0 for b in bases.values())
            ids=[heads[:lanes].copy(),heads[lanes:].copy()];groups={}
            for q in range(k):
                for ch in range(2):
                    current=ids[ch];rows=ch*(nodes+1)+current;begin=offsets[rows];degree=offsets[rows+1]-begin
                    assert np.all(degree==(1 if q<k-1 else 0))
                    accesses={'value':bases['values']+current.astype(np.uint64)*8,'tag':bases['tags']+current.astype(np.uint64)*8,
                        'csr_begin':bases['offsets']+rows.astype(np.uint64)*8,'csr_end':bases['offsets']+(rows.astype(np.uint64)+1)*8}
                    if q<k-1:accesses['csr_target']=bases['targets']+begin.astype(np.uint64)*8
                    for load,addresses in accesses.items():
                        data=summarize(addresses)
                        record={'case':case['id'],'layout':name,'q':q,'cursor':'a' if ch==0 else 'b','logical_load':load,**data}
                        if q in {0,1,k-1}:
                            first=addresses[:32];record['first_warp_byte_addresses']=[int(x) for x in first];record['first_warp_32byte_segment_ids']=sorted(set(int(x//32) for x in first))
                        records.append(record);groups.setdefault((ch,load),[]).append(data)
                    if q<k-1:ids[ch]=targets[begin]
            for (ch,load),data in groups.items():
                events=sum(x['warp_events'] for x in data)
                summaries.append({'case':case['id'],'layout':name,'cursor':'a' if ch==0 else 'b','logical_load':load,
                    'q_count':len(data),'warp_events':events,'mean_segments':sum(x['sum_segments'] for x in data)/events,
                    'mean_unique_addresses':sum(x['mean_unique_addresses']*x['warp_events'] for x in data)/events})
            print(case['id'],name,'logical address analysis complete',flush=True)
    write(a.output,{'evidence_type':'deterministic logical address analysis','quantity':'distinct 32-byte address segments per scalar logical warp access',
        'hardware_counters':'unavailable: ERR_NVGPUCTRPERM; segment counts are address quantities, hardware transactions/cache misses remain unmeasured',
        'source_sha256':sha(Path(__file__)),'input_sha256':sha(a.inputs),'profile_results_sha256':sha(a.profile),
        'scalar_bytes':8,'warp_lanes':32,'array_base_alignment_verified':256,
        'model_boundary':'Each q/cursor/load/warp is separate. Duplicated lane addresses share a segment. Compiler instruction transformations, cache state and transaction merging are outside this model.',
        'summaries':summaries,'per_q_cursor_load':records})


if __name__=='__main__':main()
