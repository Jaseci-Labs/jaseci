#!/usr/bin/env python3
"""Verified standard LLVM O2 on the identical production Dot module; full checks."""
import argparse
from pathlib import Path
import subprocess
import sys
from prepare import HERE,ROOT,read,write,sha
sys.path.insert(0,str(HERE.parent))
from compare_named_layouts import schemas_and_modules


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    from jaclang.runtime.gpu_cursors import build_cursor_module
    from jaclang.compiler.backends.native.ptx import ptx_target
    from jaclang.compiler.backends.native.llvm import binding as llvm
    schemas,_=schemas_and_modules({'Dot'});target=ptx_target();module=build_cursor_module([schemas['Dot'].cursor_spec],target)
    raw=str(module);(a.output/'raw.ll').write_text(raw)
    baseline=target.emit_assembly(module);assert baseline==(a.inputs.parent/'Dot.ptx').read_text()
    mod=llvm.parse_assembly(raw);mod.verify();pb=llvm.create_pass_builder(target,llvm.create_pipeline_tuning_options(speed_level=2));pb.getModulePassManager().run(mod,pb);mod.verify()
    (a.output/'O2.ll').write_text(str(mod));ptx=target.emit_assembly(mod);(a.output/'O2.ptx').write_text(ptx)
    command=['/usr/local/cuda-12.9/bin/ptxas','-arch=sm_86','-v',str(a.output/'O2.ptx'),'-o',str(a.output/'O2.cubin')]
    log=subprocess.run(command,check=True,capture_output=True,text=True);(a.output/'ptxas.log').write_text(log.stdout+log.stderr)
    previous=ROOT/'scripts/gpu_walker/handwritten_matmul/validation/20261021/codegen'
    assert sha(a.output/'O2.ptx')==sha(previous/'O2.ptx')
    checked=read(previous/'status-validation.json');assert checked['status']=='PASS' and checked['ptx_sha256']['O2']==sha(a.output/'O2.ptx')
    write(a.output/'codegen.json',{'pipeline':'standard LLVM O2; checked semantics retained','production_ptx_sha256':sha(a.inputs.parent/'Dot.ptx'),
        'optimized_ptx_sha256':sha(a.output/'O2.ptx'),'raw_ir_sha256':sha(a.output/'raw.ll'),'optimized_ir_sha256':sha(a.output/'O2.ll'),
        'generator_sha256':sha(Path(__file__)),'checked_error_fixtures':len(checked['cases']),'status_evidence':str((previous/'status-validation.json').relative_to(ROOT)),
        'status_evidence_sha256':sha(previous/'status-validation.json'),'compiler_source_sha256':{str(path.relative_to(ROOT)):sha(path) for path in [ROOT/'jac/jaclang/runtime/gpu_cursors.py',ROOT/'jac/jaclang/compiler/backends/native/ptx.jac']},
        'baseline_allocas':raw.count(' alloca '),'optimized_allocas':str(mod).count(' alloca '),'ptx_local_load_sites':ptx.count('ld.local.'),'ptx_local_store_sites':ptx.count('st.local.'),'ptxas_command':command,'ptxas_log':log.stdout+log.stderr})
    print('Checked O2 emitted; production baseline identical; optimized PTX matches status-validated artifact:',sha(a.output/'O2.ptx'))


if __name__=='__main__':main()
