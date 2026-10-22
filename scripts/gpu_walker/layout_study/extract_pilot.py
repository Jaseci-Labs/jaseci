#!/usr/bin/env python3
"""Extract the three-arm production-PTX pilot from its single verified source trace."""
import csv
from prepare import HERE, ROOT, read, write, sha


def main():
    folder = ROOT/'scripts/gpu_walker/handwritten_matmul/validation/20261021/profile'
    verified = read(folder/'verified-kernels.json')
    run = read(folder/'results.json')
    assert verified['status'] == 'PASS' and run['complete']
    assert verified['results_sha256'] == sha(folder/'results.json')
    assert verified['sqlite_sha256'] == sha(folder/'trace.sqlite')
    rows = []
    for cid in dict.fromkeys(s['case'] for s in verified['summaries']):
        values = [next(s['kernel_median_us'] for s in verified['summaries'] if s['case']==cid and s['arm']==arm) for arm in ['Jac Random-928','Jac Predicted','CUDA tiled']]
        b,a,r = values
        rows.append({'case':cid,'jac_before_random_us':b,'jac_after_predicted_us':a,'handwritten_tiled_reference_us':r,'layout_speedup':b/a,'residual_gap':a/r})
    out = HERE/'pilot'; out.mkdir(exist_ok=True)
    write(out/'comparison.json', {'source_run':str(folder.relative_to(ROOT)),
        'compiler_policy':'supplementary production emission before the added LLVM middle-end',
        'extractor_sha256':sha(HERE/'extract_pilot.py'),
        'source_sha256':{name:sha(folder/name) for name in ['results.json','verified-kernels.json','trace.sqlite','trace.nsys-rep']},
        'jac_ptx_sha256':run['jac_ptx_sha256'],'random_seed':928,'unit':'microseconds',
        'statistic':'median actual Nsight kernel end-start','rows':rows})
    with (out/'comparison.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=[*rows[0],'unit','source_run'],lineterminator='\n');writer.writeheader()
        for row in rows:writer.writerow({**row,'unit':'microseconds','source_run':str(folder.relative_to(ROOT))})
    print('Pilot source hashes and verified joins PASS; three-arm supplementary pilot extracted.')


if __name__=='__main__':main()
