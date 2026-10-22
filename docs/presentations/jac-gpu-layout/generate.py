#!/usr/bin/env python3
"""Build the English layout-study deck from contract-checked actual kernel samples."""
import hashlib
import json
import os
from pathlib import Path
import textwrap
os.environ.setdefault('MPLCONFIGDIR', '/tmp/jac-layout-slides-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
STUDY = ROOT/'scripts/gpu_walker/layout_study'
DATA = STUDY/'validation/20261022'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
comparison = read(DATA/'comparison.json')
validation = read(DATA/'contract-validation.json')
assert validation['status'] == 'PASS'
assert comparison['source_run_id'] == 'optimized-profile'
assert comparison['contract_sha256'] == validation['contract_sha256'] == sha(STUDY/'RESEARCH_CONTRACT.md')
assert validation['report_generator_sha256'] == sha(STUDY/'build_report.py')
assert len(comparison['primary_groups']) == 3
assert 'Random928 + checked LLVM O2' in comparison['primary_groups'][0]
assert 'Predicted + checked LLVM O2' in comparison['primary_groups'][1]
assert 'nvcc O3' in comparison['primary_groups'][2]
for name, digest in comparison['sources_sha256'].items():
    assert sha(DATA/name) == digest
verified = read(DATA/'optimized-profile/verified.json')
run = read(DATA/'optimized-profile/results.json')
rows = comparison['rows']
fields = ['jac_before_random928_o2_us', 'jac_after_predicted_o2_us', 'handwritten_cuda_o3_reference_us']
for r in rows:
    for field, arm in zip(fields, comparison['primary_groups']):
        s = next(s for s in verified['summaries'] if s['case'] == r['case'] and s['arm'] == arm)
        assert s['median_us'] == r[field] and s['sample_n'] == 240
    assert r['layout_speedup_before_after'] == r[fields[0]]/r[fields[1]]
    assert r['residual_gap_after_reference'] == r[fields[1]]/r[fields[2]]
scale = read(DATA/'scale-3000-feasibility.json')
model = read(DATA/'optimized-address-analysis.json')
segments = {(s['layout'],s['cursor'],s['logical_load']): s for s in model['summaries'] if s['case'] == rows[-1]['case']}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42})
INK, MUTED, BLUE, TEAL, ORANGE = '#17243b', '#58677b', '#2563eb', '#078477', '#c76b16'
pdf = PdfPages(OUT/'jac-gpu-layout.pdf')
pdf.infodict()['Title'] = 'Jac GPU Memory Layout: Random and Access-Order-Aware Predicted'
pages = 0

def page(title, section, subtitle='', source='optimized-profile; comparison.json'):
    global pages
    pages += 1
    f = plt.figure(figsize=(16,9), facecolor='white')
    f.text(.055,.95,'JAC ON GPU  /  '+section.upper(),fontsize=11,color=TEAL,weight='bold')
    f.text(.055,.875,title,fontsize=28,color=INK,weight='bold')
    f.text(.055,.815,subtitle,fontsize=15,color=MUTED)
    f.text(.055,.035,'2026-10-22  •  '+source,fontsize=8,color=MUTED)
    f.text(.95,.035,str(pages),fontsize=10,color=MUTED,ha='right')
    return f

def text(f,s,y=.72,size=21,width=97,color=INK):
    obj = f.text(.06,y,textwrap.fill(s,width,break_long_words=False),fontsize=size,color=color,va='top',linespacing=1.4)
    f.canvas.draw()
    while obj.get_window_extent().x1 > f.bbox.width*.95:
        width -= 2
        obj.set_text(textwrap.fill(s,width,break_long_words=False))
        f.canvas.draw()
    assert obj.get_window_extent().y0 > f.bbox.height*.06, (pages,s)

def table(f, heads, contents, bbox=(.055,.24,.89,.49), size=18, widths=None):
    ax = f.add_axes([0,0,1,1]); ax.axis('off')
    t = ax.table(cellText=contents,colLabels=heads,cellLoc='left',colLoc='left',colWidths=widths,bbox=bbox)
    t.auto_set_font_size(False); t.set_fontsize(size)
    for (r,c),cell in t.get_celld().items():
        cell.set_edgecolor('#dbe4ed'); cell.set_linewidth(.7)
        cell.set_facecolor('#e7eef8' if r==0 else '#f5f7fb' if r%2 else 'white')
        cell.set_text_props(color=INK,weight='bold' if r==0 else 'normal')
    f.canvas.draw()
    for cell in t.get_celld().values():
        obj = cell.get_text(); original = obj.get_text()
        width = max(map(len,original.split('\n')))
        while obj.get_window_extent().width > cell.get_window_extent().width*.90:
            width -= 1
            obj.set_text('\n'.join(textwrap.fill(line,width,break_long_words=False) for line in original.split('\n')))
            f.canvas.draw()
        assert obj.get_window_extent().height < cell.get_window_extent().height*.98, (pages,original)

def save(f):
    pdf.savefig(f); plt.close(f)

r=rows[-1]
f=page('Can Jac access order guide GPU memory layout?', 'Research question',
    'Primary variable: node layout • same checked LLVM O2 kernel for both Jac arms')
text(f,'BEFORE: Jac Random928 + checked LLVM O2',y=.71,size=25)
text(f,'AFTER: Jac Predicted + identical checked LLVM O2 PTX',y=.60,size=25)
text(f,'REFERENCE: fixed handwritten tiled CUDA, nvcc O3',y=.49,size=25)
text(f,f"256³: {r[fields[0]]:.3f} → {r[fields[1]]:.3f} µs; layout speedup {r['layout_speedup_before_after']:.3f}×.",y=.32,size=26,color=TEAL)
text(f,f"Predicted / handwritten: {r['residual_gap_after_reference']:.2f}×. Full output/status validation on a shared RTX 3090.",y=.18,size=19,width=115,color=MUTED)
save(f)

f=page('Place nodes in their known discovery order','Layout strategy',
    'C[i,j] = Σq A[i,q] × B[q,j] • one Jac GPU lane per output')
text(f,'Predicted concatenates complete cursor-a BFS and complete cursor-b BFS: all A nodes, then all B nodes.',size=23,width=90)
table(f,['Physical ID order','Logical node sequence'],[
    ['Random928','Fixed seeded permutation of all A and B identities'],
    ['Predicted: cursor a','A[0,0], A[1,0], … ; A[0,1], A[1,1], …'],
    ['Predicted: cursor b','B[0,0], B[0,1], … ; B[1,0], B[1,1], …'],
],bbox=(.055,.30,.89,.30),size=18,widths=[.29,.71])
text(f,'Values, tags, CSR rows/targets, heads and initialized queues are remapped consistently. Saved bijections and every q/cursor/lane arrival preserve logical identity.',y=.23,size=18,width=116)
text(f,'Jac source, arithmetic, queue/visit limits, lane mapping and grid/block stay fixed.',y=.10,size=17,width=120,color=MUTED)
save(f)

f=page('A matched optimizing policy and resident metric','Protocol',
    'LLVM O2 and nvcc O3 are distinct optimizing pipelines with different guarantees.')
text(f,'Jac: same production raw LLVM → standard checked LLVM O2 → existing target codegen. Both layouts reuse one loaded function.',size=21,width=94)
text(f,'CUDA: fixed 16 × 16 shared-memory tiled int64 kernel, nvcc -O3. The same kernel handles all five sizes.',y=.54,size=21,width=94)
text(f,'One randomized interleaved run: 3 warmup rounds, then 15 rounds × 16 graph nodes per cell. Actual Nsight node-kernel end − start is the primary metric.',y=.37,size=21,width=94)
text(f,'Packing, transfers, poisoning and verification are separate from resident kernel time. Shared RTX 3090; Ollama held approximately 23,462 MiB.',y=.16,size=17,width=117,color=MUTED)
save(f)

f=page('Three primary groups, full matmul coverage','Measured result',
    'Median actual kernel duration (µs), 240 samples per cell; lower is faster.')
table(f,['M × K × N','Jac BEFORE\nRandom + O2','Jac AFTER\nPredicted + O2','REFERENCE\nTiled CUDA O3'],[
    [f"{x['M']} × {x['K']} × {x['N']}",*[f'{x[k]:,.3f}' for k in fields]] for x in rows
],bbox=(.055,.26,.89,.48),size=19,widths=[.27,.24,.25,.24])
text(f,'All three columns share one fresh randomized interleaved trace: optimized-profile.',y=.18,size=18,width=115)
text(f,'Jac uses 128 threads/block. CUDA uses its fixed 16 × 16 tile geometry.',y=.10,size=17,width=120,color=MUTED)
save(f)

f=page('Layout benefit depends on workload size','Measured ratios',
    'Before / after > 1 means layout improves Jac; after / reference is the residual gap.')
table(f,['M × K × N','Layout speedup\nRandom / Predicted','Residual gap\nPredicted / CUDA'],[
    [f"{x['M']} × {x['K']} × {x['N']}",f"{x['layout_speedup_before_after']:.3f}×",f"{x['residual_gap_after_reference']:.2f}×"] for x in rows
],bbox=(.055,.29,.89,.44),size=20,widths=[.30,.35,.35])
text(f,'Seeds 928, 929 and 930 agree on direction at each size: regression on the two smallest cases, improvement on the three larger cases.',y=.23,size=19,width=106)
text(f,'Raw samples, p10/p90 and paired-round means are retained. The separate ordinary-event run gives the same directions.',y=.13,size=16,width=120,color=MUTED)
save(f)

f=page('Address organization is directly reproducible','Interpretation',
    'Deterministic logical address analysis • 256³ • mean 32-byte segments per warp access')
loads=[('a','value'),('b','value'),('b','csr_begin'),('b','csr_target')]
table(f,['Logical access','Random928','Predicted'],[
    [f'Cursor {c}: {load}',*[f"{segments[layout,c,load]['mean_segments']:.3f}" for layout in ['before','after']]] for c,load in loads
],bbox=(.055,.39,.89,.30),size=20,widths=[.50,.25,.25])
text(f,'At N=256, lanes share one A node and access 32 distinct B nodes. Predicted makes those B-node addresses consecutive.',y=.31,size=20,width=103)
text(f,'Nsight Compute returned ERR_NVGPUCTRPERM. Segment counts model logical addresses; hardware transactions, cache misses and occupancy remain unmeasured. Hardware attribution stays unresolved.',y=.18,size=17,width=120,color=MUTED)
save(f)

f=page('Correctness and launch evidence','Validation',
    'Byte-identical checked O2 artifact for both Jac layouts; every replay checked')
table(f,['Evidence','Result'],[
    ['Logical graph and traversal equivalence','All fields, edges, heads, permutations and lane arrivals pass'],
    ['Full normal-case outputs/statuses','Poison → replay → check all M×N values and Jac statuses'],
    ['Prior error/status validation, identical PTX','13 O2 fixtures match production host JIT'],
    ['Independent Nsight launch join','7,225 launches; 6,000 measured; 3,600 primary nodes'],
],bbox=(.055,.29,.89,.44),size=18,widths=[.43,.57])
text(f,'Error fixtures cover overflow, invalid node/CSR, queue capacity and round limits. Fresh output checks use NumPy int64 plus the saved oracle.',y=.23,size=18,width=112)
text(f,'Both optimizing pipelines retain their execution contracts. The remaining CUDA gap compares complete implementations.',y=.13,size=16,width=120,color=MUTED)
save(f)

f=page('3000³: separate correctness, timing and capacity','Scale boundary',
    'Historical evidence uses its own older PTX/data and 32,768-output timed subsets.')
text(f,'Historical full correctness: 9,000,000 outputs. Historical resident subset medians: Random 70.802 ms, Predicted 8.973 ms (7.89×); handwritten timing absent.',y=.71,size=22,width=93)
text(f,f"One packed graph: {scale['graph_bytes_per_layout']/1e6:.2f} MB. This run: {scale['current_free_bytes_after_context']/1e6:.2f} MB free after context creation.",y=.50,size=22,width=93)
text(f,'A paired full-coverage follow-up needs about 1.66 GB plus allocation/JIT headroom, then all 275 bounded Jac batches and matched tiled output coverage.',y=.33,size=22,width=93)
text(f,'Evidence: scripts/gpu_walker/layout_study/validation/20261022/REPORT.md and comparison.csv. Reproduce with layout_study/reproduce.sh; deck source hashes are in sources.json.',y=.14,size=17,width=120,color=MUTED)
save(f)
pdf.close()
paths=[DATA/'comparison.json',DATA/'REPORT.md',DATA/'contract-validation.json',DATA/'optimized-profile/verified.json',DATA/'optimized-codegen/codegen.json',DATA/'optimized-address-analysis.json',STUDY/'RESEARCH_CONTRACT.md',Path(__file__)]
(OUT/'sources.json').write_text(json.dumps({'source_run_id':'optimized-profile','primary_groups':comparison['primary_groups'],'files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in paths]},indent=2)+'\n')
print(f'Built {pages} slides: {OUT/"jac-gpu-layout.pdf"}')
