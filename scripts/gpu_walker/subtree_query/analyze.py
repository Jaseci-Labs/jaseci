#!/usr/bin/env python3
"""Verify every Nsight kernel launch and retain actual timing distributions."""
import argparse
import sqlite3
import statistics
from common import read, sha, write
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('results',type=Path);p.add_argument('sqlite',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();d=read(a.results);assert d['complete']
    expected=[]
    for case in d['cases']:
        for arm in case['arms']:
            expected.append((case['id'],arm,'prime',-1,0))
        for record in d['records']:
            if record['case']==case['id']:
                expected.extend((record['case'],record['arm'],record['phase'],record['pair'],node) for node in range(d['inner']))
    with sqlite3.connect(a.sqlite) as db:
        rows=db.execute('SELECT k.start,k.end,s.value,k.gridX,k.gridY,k.gridZ,k.blockX,k.blockY,k.blockZ,k.contextId,k.correlationId FROM CUPTI_ACTIVITY_KIND_KERNEL k JOIN StringIds s ON s.id=k.shortName ORDER BY k.start').fetchall()
    assert len(rows)==len(expected),(len(rows),len(expected))
    cases={x['id']:x for x in d['cases']};samples=[]
    for index,(identity,row) in enumerate(zip(expected,rows)):
        case,arm,phase,pair,node=identity
        launch=cases[case]['arms'][arm]
        assert row[2]==launch['kernel'],(index,identity,row)
        assert tuple(row[3:9])==tuple(launch['grid']+launch['block']),(index,identity,row)
        assert row[1]>row[0]
        samples.append({'launch_index':index,'case':case,'arm':arm,'phase':phase,'pair':pair,'graph_node':node,'kernel':row[2],
            'start_ns':row[0],'end_ns':row[1],'context':row[9],'correlation_id':row[10],'kernel_us':(row[1]-row[0])/1000})
    summaries=[]
    for case in d['cases']:
        for arm in case['arms']:
            vals=[x['kernel_us'] for x in samples if x['case']==case['id'] and x['arm']==arm and x['phase']=='measured']
            assert len(vals)==d['inner']*d['repeats']
            pair_means=[statistics.mean(x['kernel_us'] for x in samples if x['case']==case['id'] and x['arm']==arm and x['phase']=='measured' and x['pair']==pair) for pair in range(d['repeats'])]
            ordered=sorted(vals)
            summaries.append({'case':case['id'],'arm':arm,'median_us':statistics.median(vals),'min_us':min(vals),'max_us':max(vals),
                'p10_us':ordered[int(.1*(len(ordered)-1))],'p90_us':ordered[int(.9*(len(ordered)-1))],
                'sample_n':len(vals),'pair_mean_us':pair_means,'median_pair_mean_us':statistics.median(pair_means)})
    result={'status':'PASS','analyzer_sha256':sha(Path(__file__)),'results_sha256':sha(a.results),'sqlite_sha256':sha(a.sqlite),
        'metric':'actual kernel end-start in microseconds; each node traced independently',
        'launches_verified':len(rows),'measured_launches':sum(x['phase']=='measured' for x in samples),
        'contexts':sorted(set(x['context'] for x in samples)),'summaries':summaries,'samples':samples}
    write(a.output,result)
    print({k:v for k,v in result.items() if k not in ('summaries','samples')})


if __name__=='__main__':
    main()
