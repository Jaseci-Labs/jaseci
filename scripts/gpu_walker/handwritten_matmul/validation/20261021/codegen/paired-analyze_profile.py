#!/usr/bin/env python3
"""Join every Nsight kernel to its exact case/arm and verify launch coverage."""
import argparse, hashlib, json, sqlite3, statistics
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);p.add_argument('sqlite',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 d=json.loads(a.results.read_text());expected=[]
 for case in d['cases']:
  for arm in case['arms']:expected.append((case['id'],arm,'prime',-1))
  for r in d['records']:
   if r['case']==case['id']:expected.extend([(r['case'],r['arm'],r['phase'],r['pair'])]*d['inner'])
 with sqlite3.connect(a.sqlite) as db:
  rows=db.execute('SELECT k.start,k.end,s.value,k.gridX,k.gridY,k.gridZ,k.blockX,k.blockY,k.blockZ FROM CUPTI_ACTIVITY_KIND_KERNEL k JOIN StringIds s ON s.id=k.shortName ORDER BY k.start').fetchall()
 assert len(rows)==len(expected),(len(rows),len(expected))
 samples=[];cases={r['id']:r for r in d['cases']}
 for index,((case,arm,phase,pair),row) in enumerate(zip(expected,rows)):
  name='jac_Dot_cursors_batch' if arm.startswith('Jac ') else 'matmul_'+arm.split()[-1]+'_i64'
  assert row[2]==name,(index,case,arm,row[2],name)
  m,k,n=cases[case]['shape'];geometry=((m*n+127)//128,1,1,128,1,1) if arm.startswith('Jac ') else ((n+15)//16,(m+15)//16,1,16,16,1)
  assert tuple(row[3:])==geometry,(index,row,geometry)
  assert row[1]>row[0]
  samples.append(dict(case=case,arm=arm,phase=phase,pair=pair,kernel=name,kernel_us=(row[1]-row[0])/1000))
 summaries=[]
 for case in d['cases']:
  for arm in case['arms']:
   vals=[r['kernel_us'] for r in samples if r['case']==case['id'] and r['arm']==arm and r['phase']=='measured']
   assert len(vals)==d['inner']*d['repeats']
   bypair=[sum(r['kernel_us'] for r in samples if r['case']==case['id'] and r['arm']==arm and r['phase']=='measured' and r['pair']==i)/d['inner'] for i in range(d['repeats'])]
   summaries.append(dict(case=case['id'],arm=arm,kernel_median_us=statistics.median(vals),kernel_min_us=min(vals),kernel_max_us=max(vals),sample_n=len(vals),median_pair_mean_kernel_us=statistics.median(bypair)))
 result={'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'PASS','measurement':'Nsight Systems actual kernel end-start; excludes graph scheduling gaps, copies and host work','launches_verified':len(rows),'measured_launches':sum(r['phase']=='measured' for r in samples),'results_sha256':hashlib.sha256(a.results.read_bytes()).hexdigest(),'sqlite_sha256':hashlib.sha256(a.sqlite.read_bytes()).hexdigest(),'summaries':summaries,'samples':samples}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['samples','summaries']}))
if __name__=='__main__':main()
