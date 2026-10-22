#!/usr/bin/env python3
"""Record exact source hashes and optionally the completed subtree command list."""
import argparse
import platform
from pathlib import Path
import shlex
import subprocess
from common import HERE, ROOT, read, sha, write


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('validation',type=Path);p.add_argument('--write-commands',action='store_true');a=p.parse_args();v=a.validation
    compiler=[ROOT/'jac/examples/gpu/subtree_query.jac',
        ROOT/'jac/jaclang/compiler/backends/native/ptx_csr.jac',
        ROOT/'jac/jaclang/compiler/backends/native/ptx_walker.jac',
        ROOT/'jac/jaclang/compiler/backends/native/ptx.jac',
        ROOT/'jac/jaclang/runtime/gpu.jac',ROOT/'jac/jaclang/runtime/gpu_memory.jac',
        ROOT/'jac/jaclang/compiler/backends/native/llvm/libjacllvm.so',
        HERE.parent/'handwritten_matmul/benchmark.py',HERE.parent/'compare_layouts.py']
    source=sorted([*HERE.glob('*.py'),*HERE.glob('*.cu'),*HERE.glob('*.sh'),*compiler])
    report={'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        'origin':subprocess.check_output(['git','remote','get-url','origin'],cwd=ROOT,text=True).strip(),
        'python':platform.python_version(),'nvcc':subprocess.check_output(['/usr/local/cuda-12.9/bin/nvcc','--version'],text=True),
        'nsys':subprocess.check_output(['/usr/local/bin/nsys','--version'],text=True),
        'primary_run':'profile','supplementary_run':'ablation-profile','input_manifest_sha256':sha(v/'inputs.json'),
        'source_sha256':{str(path.relative_to(ROOT)):sha(path) for path in source},
        'raw_evidence_sha256':{str(path.relative_to(v)):sha(path) for path in [v/'profile/results.json',v/'profile/verified.json',v/'profile/trace.nsys-rep',v/'profile/trace.sqlite',v/'ablation-profile/results.json',v/'ablation-profile/verified.json',v/'ablation-profile/trace.nsys-rep',v/'ablation-profile/trace.sqlite',v/'correctness.json']}}
    write(v/'provenance.json',report)
    if a.write_commands:
        src=HERE.relative_to(ROOT)
        commands=[['env/bin/python',str(src/'common.py'),'--probe',str(v/'memory-probe.json')],
                  ['env/bin/python',str(src/'prepare.py'),'--output',str(v),'--memory-probe',str(v/'memory-probe.json')],
                  ['env/bin/python',str(src/'run.py'),'--inputs',str(v/'inputs.json'),'--output',str(v/'ordinary')]]
        for name,flags in [('profile',[]),('ablation-profile',['--ablations'])]:
            if flags:
                commands.append(['env/bin/python',str(src/'run.py'),'--inputs',str(v/'inputs.json'),'--output',str(v/'ablation-ordinary'),*flags,'--warmup','3','--repeats','15'])
            commands.append(['/usr/local/bin/nsys','profile','--trace=cuda','--cuda-graph-trace=node','--sample=none','--cpuctxsw=none','--force-overwrite=true','--output',str(v/name/'trace'),'env/bin/python',str(src/'run.py'),'--inputs',str(v/'inputs.json'),'--output',str(v/name),*flags,'--warmup','3','--repeats','15'])
            commands.append(['/usr/local/bin/nsys','export','--type','sqlite','--force-overwrite=true','--output',str(v/name/'trace.sqlite'),str(v/name/'trace.nsys-rep')])
            commands.append(['env/bin/python',str(src/'analyze.py'),str(v/name/'results.json'),str(v/name/'trace.sqlite'),'--output',str(v/name/'verified.json')])
        commands += [['env/bin/python',str(src/'validate.py'),'--validation',str(v)],
                     ['env/bin/python','-m','unittest','discover','-s','scripts/gpu_walker','-p','test_subtree.py','-v'],
                     ['env/bin/python',str(src/'build_report.py'),str(v)],
                     ['env/bin/python','docs/presentations/jac-gpu-subtree/generate.py'],
                     ['env/bin/python',str(src/'record_provenance.py'),str(v),'--write-commands']]
        (v/'commands.txt').write_text('# Completed final commands, repository root; PYTHONPATH=jac:scripts/gpu_walker for Jac compiler/CPU commands.\n# Reports use one interleaved primary run and one separate interleaved ablation run.\n'+'\n'.join(shlex.join(cmd) for cmd in commands)+'\n')
    print('Source and raw-evidence provenance recorded.')


if __name__=='__main__':main()
