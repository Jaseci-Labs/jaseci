#!/usr/bin/env python3
"""Collect one checked-O2 counter probe; retain access errors and full validation."""
import argparse
from pathlib import Path
import subprocess
import sys
from prepare import HERE, read, write, sha


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('validation',type=Path);v=p.parse_args().validation
    folder=v/'counters';folder.mkdir(exist_ok=True)
    metric='l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum'
    command=['/opt/nvidia/nsight-compute/2025.3.0/ncu','--target-processes','all','--kernel-name','regex:jac_Dot_cursors_batch','--launch-count','1','--metrics',metric,'--force-overwrite','--export',str(folder/'o2-random928'),sys.executable,str(HERE/'run.py'),'--inputs',str(v/'inputs/inputs.json'),'--jac-ptx',str(v/'optimized-codegen/O2.ptx'),'--output',str(folder/'o2-probe'),'--case-id','matmul-256x256x256','--only-arm','before','--warmup','0','--repeats','1','--inner','1']
    with (folder/'o2-ncu.log').open('w') as f:
        result=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
    text=(folder/'o2-ncu.log').read_text()
    denied='ERR_NVGPUCTRPERM' in text
    write(folder/'o2-status.json',{'status':'unavailable' if denied else 'collected' if result.returncode==0 else 'failed','error':'ERR_NVGPUCTRPERM' if denied else None,
        'exit_code':result.returncode,'log':'o2-ncu.log','log_sha256':sha(folder/'o2-ncu.log'),'requested_metric':metric,'command':command,
        'probe_case':'matmul-256x256x256','probe_arm':'Jac before (Random928 + checked LLVM O2)','timing_usage':'separate counter probe; primary timings from optimized-profile'})
    assert read(folder/'o2-probe/results.json')['complete']
    assert result.returncode==0 or denied


if __name__=='__main__':main()
