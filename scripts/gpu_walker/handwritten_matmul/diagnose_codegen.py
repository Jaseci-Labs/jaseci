#!/usr/bin/env python3
"""Reproducible LLVM-only Dot ablations; production compiler is untouched.

Checked variants keep the complete walker ABI and all error paths. No-check
variants deliberately narrow the contract to the validated benchmark fixtures;
they are diagnostic controls, not compiler fixes.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from compare_named_layouts import schemas_and_modules


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def hoist_scalar_allocas(text):
    """Fixed-size nonescaping scalar allocas can be promoted at function entry."""
    lines = text.splitlines()
    allocas = [line for line in lines if ' alloca ' in line]
    assert len(allocas) == 10
    assert all(re.search(r'alloca i64(?:, align 8)?$', line) for line in allocas)
    lines = [line for line in lines if ' alloca ' not in line]
    entry = next(i for i, line in enumerate(lines) if line == 'entry:')
    lines[entry + 1:entry + 1] = allocas
    return '\n'.join(lines) + '\n'


def bypass_errors(text, codes):
    changed = 0
    pattern = r'(?m)^\s*br i1 [^\n]+, label %([\w.]+), label %([\w.]+)$'
    def replace(match):
        nonlocal changed
        a, b = match.groups()
        if b in {f'error.{code}' for code in codes}:
            changed += 1
            return f'  br label %{a}'
        if a in {f'error.{code}' for code in codes}:
            changed += 1
            return f'  br label %{b}'
        return match.group()
    result = re.sub(pattern, replace, text)
    assert changed > 0
    return result, changed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--baseline-ptx', type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    from jaclang.runtime.gpu_cursors import build_cursor_module
    from jaclang.compiler.backends.native.ptx import ptx_target
    from jaclang.compiler.backends.native.llvm import binding as llvm
    schemas, _ = schemas_and_modules({'Dot'})
    target = ptx_target()
    module = build_cursor_module([schemas['Dot'].cursor_spec], target)
    raw = str(module)  # emit_assembly also mutates its input: retain raw IR first.
    baseline = target.emit_assembly(module)
    assert baseline == a.baseline_ptx.read_text(), 'Baseline differs from measured production PTX'
    (a.output / 'input.ll').write_text(raw)
    result = {'generator_sha256': digest(Path(__file__).read_text()),
              'input_ir_sha256': digest(raw), 'baseline_ptx_sha256': digest(baseline),
              'IR_files': 'Verified middle-end IR before target.emit_assembly (which may mutate IR)',
              'transformations': {}}
    labels = ['baseline', 'sroa', 'hoist_sroa', 'O2', 'O2_no_overflow',
              'O2_no_validation', 'O2_unchecked']
    for label in labels:
        text = hoist_scalar_allocas(raw) if label == 'hoist_sroa' else raw
        bypassed = 0
        codes = {'O2_no_overflow': [3], 'O2_no_validation': [1, 2, 5, 6],
                 'O2_unchecked': [1, 2, 3, 5, 6]}.get(label, [])
        if codes:
            text, bypassed = bypass_errors(text, codes)
        mod = llvm.parse_assembly(text)
        mod.verify()
        pto = llvm.create_pipeline_tuning_options(speed_level=2)
        pb = llvm.create_pass_builder(target, pto)
        if label in ('sroa', 'hoist_sroa'):
            pm = llvm.ModulePassManager()
            pm.add_sroa_pass()
            pm.run(mod, pb)
        elif label.startswith('O2'):
            pb.getModulePassManager().run(mod, pb)
        mod.verify()
        ir = str(mod)
        (a.output / (label + '.ll')).write_text(ir)
        ptx = target.emit_assembly(mod)
        (a.output / (label + '.ptx')).write_text(ptx)
        cmd = ['/usr/local/cuda-12.9/bin/ptxas', '-arch=sm_86', '-v',
               str(a.output / (label + '.ptx')), '-o', str(a.output / (label + '.cubin'))]
        log = subprocess.run(cmd, check=True, capture_output=True, text=True)
        (a.output / (label + '-ptxas.log')).write_text(log.stdout + log.stderr)
        result['transformations'][label] = {
            'ptx_sha256': digest(ptx), 'IR_alloca_instructions': ir.count(' alloca '),
            'PTX_local_loads': ptx.count('ld.local.'), 'PTX_local_stores': ptx.count('st.local.'),
            'PTX_global_loads': ptx.count('ld.global.'), 'PTX_global_stores': ptx.count('st.global.'),
            'bypassed_error_codes': codes, 'bypassed_branches': bypassed,
            'ptxas_command': cmd, 'ptxas': log.stdout + log.stderr}
        print(label, result['transformations'][label], flush=True)
    (a.output / 'codegen.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
