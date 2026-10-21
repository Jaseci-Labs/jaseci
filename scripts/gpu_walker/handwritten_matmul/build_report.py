#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('ordinary',type=Path);p.add_argument('profile',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
d=json.loads(a.ordinary.read_text());prof=json.loads(a.profile.read_text());assert d['complete'] and prof['status']=='PASS'
index={(r['case'],r['arm']):r for r in prof['summaries']}
lines=['# Handwritten CUDA matmul versus Jac GPU','','All methods compute every output using the same signed int64 matrices. Each input node in Jac stores one integer.','',
'## Actual kernel durations','',
'Nsight Systems median `kernel.end - kernel.start`, microseconds per launch. This is a separately profiled run.','',
'| M × K × N | CUDA naive | CUDA tiled | Jac Current | Jac Predicted | Jac Random 928 | Predicted / tiled |',
'|---|---:|---:|---:|---:|---:|---:|']
for case in d['cases']:
 if case['dense_only']:continue
 vals=[index[(case['id'],arm)]['kernel_median_us'] for arm in ['CUDA naive','CUDA tiled','Jac Current','Jac Predicted','Jac Random-928']]
 lines.append('| '+' × '.join(map(str,case['shape']))+' | '+' | '.join(f'{v:.3f}' for v in vals)+f' | {vals[3]/vals[1]:.2f}× |')
lines+=['','## Ordinary CUDA-event graph replay','','Microseconds per kernel invocation. Each replay contains '+str(d['inner'])+' sequential kernels; the event interval is divided by that number. This includes GPU graph scheduling gaps. Allocation, compilation, graph packing, upload, download and CPU verification are outside this interval.','',
'| M × K × N | CUDA naive | CUDA tiled | Jac Current | Jac Predicted | Jac Random 928 |','|---|---:|---:|---:|---:|---:|']
for case in d['cases']:
 if case['dense_only']:continue
 vals=[case['arms'][arm]['median_us'] for arm in ['CUDA naive','CUDA tiled','Jac Current','Jac Predicted','Jac Random-928']]
 lines.append('| '+' × '.join(map(str,case['shape']))+' | '+' | '.join(f'{v:.3f}' for v in vals)+' |')
lines+=['','## Execution and correctness','',
f"- GPU: {d['gpu_name']}. Ollama held 23,462 MiB in the before/after snapshots; these are shared-GPU measurements.",
f"- Ordinary replay: {d['warmup']} warmup and {d['repeats']} measured rounds, randomized arm order with seed {d['seed']}.",
f"- Nsight launch-order/name/grid/block verification: {prof['launches_verified']} launches; {prof['measured_launches']} measured launches.",
'- Every replay checks every output against a NumPy int64 oracle; every Jac lane must also return status zero.',
'- Before timing, every packed graph cursor chain is walked on the CPU and its values are checked against the dense A and B inputs. Saved input and expected-output SHA-256 hashes are checked.',
'- Inputs include negative values and ragged dimensions. Magnitudes satisfy |A| <= 3 and |B| <= 5, so every product and partial sum fits signed int64 (absolute partial sum <= 15*K).','',
'## What the comparison measures','',
'The dense naive kernel computes one dot product per thread using address arithmetic. The tiled kernel cooperatively loads 16×16 A/B tiles into shared memory and reuses them across threads.',
'',
'Jac runs the actual compiled two-cursor Dot walker on shared Scalar/RowNext/ColumnNext graph inputs. It performs graph traversal and the generated queue, type and arithmetic checks. The dense kernels use fixed matrix dimensions and the proven input bounds. The measured ratio compares these complete implementations; it combines representation, generated execution machinery and dense tiling effects.',
'',
'Current, Predicted and Random keep the same graph semantics and lane order. Their differences are physical layout. Timings alone establish execution cost; hardware-counter attribution requires separate measurements.','',
'## Artifacts','',
'- `ordinary/results.json`: all unprofiled samples and checksums.',
'- `profile/results.json`: exact profiled request order.',
'- `profile/verified-kernels.json`: every actual kernel duration and the independent profiler join.',
'- `profile/trace.nsys-rep` / `profile/trace.sqlite`: raw profiler artifacts.',
'- `inputs/`: real Jac packed graph arrays, oracle outputs and original generated PTX.',
'- `matmul.cu`: handwritten dense kernels.','']
a.output.write_text('\n'.join(lines))
