"""Generate the English GPU matmul PDF from checked-in measurements."""
import hashlib
import json
import os
from pathlib import Path
import textwrap

os.environ.setdefault('MPLCONFIGDIR', '/tmp/jac-matmul-slides-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DATA = ROOT / 'scripts/gpu_walker/handwritten_matmul/validation/20261021'
comparison = json.loads((DATA/'primary/comparison.json').read_text())
for record in comparison['sources'].values():
    assert hashlib.sha256((DATA/record['path']).read_bytes()).hexdigest() == record['sha256']
rows = comparison['comparisons']
codegen = json.loads((DATA/'codegen/codegen.json').read_text())['transformations']
verified = json.loads((DATA/'codegen/paired-profile/verified-kernels.json').read_text())
for row in rows:
    for field, arm in [('jac_original_us', 'Jac Predicted'), ('jac_optimized_us', 'Jac O2 Predicted'), ('handwritten_us', 'CUDA tiled')]:
        measured = next(x for x in verified['summaries'] if x['case']==row['case'] and x['arm']==arm)
        assert measured['kernel_median_us'] == row[field] and measured['sample_n'] == 240
plt.rcParams.update({'font.family':'DejaVu Sans', 'pdf.fonttype':42})
INK, MUTED, BLUE, TEAL, ORANGE = '#17243b', '#59677c', '#2563eb', '#078477', '#c76b16'
pdf = PdfPages(OUT/'jac-gpu-matmul.pdf')
pdf.infodict()['Title'] = 'Jac on GPU: Matmul Performance and Compiler Diagnosis'
number = 0
def page(title, section, subtitle='', source='primary/comparison.json; codegen/paired-profile'):
    global number
    number += 1
    f = plt.figure(figsize=(16,9), facecolor='white')
    f.text(.055,.95,'JAC ON GPU  /  '+section.upper(),fontsize=11,color=TEAL,weight='bold')
    f.text(.055,.875,title,fontsize=28,color=INK,weight='bold')
    f.text(.055,.815,subtitle,fontsize=15,color=MUTED)
    f.text(.055,.035,'2026-10-21  •  '+source,fontsize=8,color=MUTED)
    f.text(.95,.035,str(number),fontsize=10,color=MUTED,ha='right')
    return f
def text(f, s, y=.71, size=22, width=86, x=.06, color=INK):
    f.text(x,y,textwrap.fill(s,width,break_long_words=False),fontsize=size,color=color,va='top',linespacing=1.45)
def table(f, heads, contents, bbox=(.055,.22,.89,.50), size=20, widths=None):
    ax=f.add_axes([0,0,1,1]);ax.axis('off')
    t=ax.table(cellText=contents,colLabels=heads,cellLoc='left',colLoc='left',colWidths=widths,bbox=bbox)
    t.auto_set_font_size(False);t.set_fontsize(size)
    for (r,c),cell in t.get_celld().items():
        cell.set_edgecolor('#dbe4ed');cell.set_linewidth(.7)
        cell.set_facecolor('#e7eef8' if r==0 else '#f5f7fb' if r%2 else 'white')
        cell.set_text_props(color=INK,weight='bold' if r==0 else 'normal')
def flow(f, labels, y=.38):
    ax=f.add_axes([.055,y,.89,.23]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    n=len(labels)
    for i,label in enumerate(labels):
        x=i/n+.02;w=1/n-.04
        ax.add_patch(FancyBboxPatch((x,.15),w,.7,boxstyle='round,pad=.012',facecolor='#edf3fc',edgecolor='#a7bad4'))
        ax.text(x+w/2,.5,label,ha='center',va='center',fontsize=18,color=INK)
        if i<n-1:ax.annotate('',xy=((i+1)/n+.005,.5),xytext=(x+w+.01,.5),arrowprops={'arrowstyle':'->','color':BLUE,'lw':2})
def save(f):
    pdf.savefig(f);plt.close(f)

f=page('Jac on GPU: Matmul','Research problem','Original Jac • checked compiler optimization • handwritten CUDA')
text(f,'How much performance can compiler optimization recover when every graph node stores one integer?',size=30,width=65)
text(f,'Separate a removable compiler cost from the remaining cost of general graph execution.',y=.43,size=23,width=80)
text(f,'Measured on RTX 3090 • int64 arithmetic • full output validation',y=.20,size=17,color=MUTED)
save(f)

f=page('One output is a paired graph traversal','Problem example','C[i, j] = Σq A[i, q] × B[q, j]',source='prepare_inputs.py; benchmark.py; saved inputs/')
flow(f,['A[i, 0]\nB[0, j]','A[i, 1]\nB[1, j]','…','A[i, K−1]\nB[K−1, j]'],y=.44)
text(f,'A cursor follows RowNext; B follows ColumnNext. Each paired arrival contributes one product to the output.',y=.72,size=21,width=95)
text(f,'The production packer creates the input graph. A GPU lane performs a complete dot product; M × N lanes produce C.',y=.31,size=21,width=95)
text(f,'Both Jac groups reuse identical packed arrays, seeds, lane order and launch geometry.',y=.16,size=17,color=MUTED,width=110)
save(f)

f=page('Three implementations, one arithmetic task','Solution','Jac layout is fixed to Predicted in the primary comparison.')
table(f,['Implementation','Execution strategy'],[
 ['Jac: no added optimization','Production LLVM → existing target codegen → PTX'],
 ['Jac: with optimization','Same LLVM → checked LLVM O2 → target codegen → PTX'],
 ['Handwritten CUDA','Fixed 16 × 16 shared-memory tiled int64 kernel'],
],bbox=(.055,.31,.89,.40),size=20,widths=[.34,.66])
text(f,'Checked O2 retains queues, type dispatch, overflow/bounds checks and status behavior. This compilation path is experimental.',y=.23,size=18,width=110)
text(f,'The CUDA implementation uses dense arrays and cooperative tile reuse.',y=.12,size=18,width=110)
save(f)

f=page('Optimization promotes cursor state to registers','Solution example','A focused compiler transformation nearly reproduces the O2 result.',source='codegen/codegen.json; status-validation.json; ABLATIONS.md')
flow(f,['10 scalar allocas\nin start block','Hoist to entry\nthen run SROA','Scalar state\npromoted'],y=.48)
table(f,['Loaded kernel / static PTX','Original','Checked O2'],[
 ['Local bytes per thread','80','0'],['Registers per thread','28','40'],
 ['Static local loads / stores','20 / 20','0 / 0'],
],bbox=(.055,.15,.89,.28),size=19,widths=[.56,.22,.22])
text(f,'SROA alone leaves PTX unchanged. Offline ptxas reports zero register spills in both variants.',y=.74,size=18,width=110)
save(f)

f=page('Measurement: actual resident kernel duration','Data / protocol','All primary cells come from one interleaved Nsight Systems run.')
text(f,'1. Use the same int64 A/B values and validate every output against NumPy.',y=.72,size=22,width=95)
text(f,'2. Randomize implementation order each round; collect 240 kernel samples per cell after warmup.',y=.56,size=22,width=95)
text(f,'3. Report median GPU kernel end − start. Allocations, transfers, CPU work and graph scheduling gaps are outside this interval.',y=.38,size=22,width=95)
text(f,'RTX 3090 • CUDA 12.9 • shared GPU: Ollama held approximately 22.9 GiB. Ratios use the interleaved run; absolute times reflect this environment.',y=.18,size=17,width=117,color=MUTED)
save(f)

f=page('Three-way performance comparison','Data','Median actual GPU kernel time in microseconds (µs); lower is faster.')
table(f,['M × K × N','Jac original','Jac + checked O2','Handwritten'],[
 [f"{r['M']} × {r['K']} × {r['N']}",*[f"{r[k]:,.3f}" for k in ['jac_original_us','jac_optimized_us','handwritten_us']]] for r in rows
],bbox=(.055,.26,.89,.48),size=20,widths=[.28,.24,.25,.23])
r=rows[-1]
text(f,f"256³: {r['jac_original_us']/r['jac_optimized_us']:.2f}× faster after O2; optimized Jac / handwritten = {r['jac_optimized_us']/r['handwritten_us']:.2f}×.",y=.17,size=22,width=110)
save(f)

f=page('At 256³, O2 recovers a substantial compiler cost','Data','The same fixed handwritten tiled kernel is used for every matrix shape.')
ax=f.add_axes([.23,.26,.66,.43])
values=[r['jac_original_us'],r['jac_optimized_us'],r['handwritten_us']]
ax.barh([2,1,0],values,color=[BLUE,TEAL,ORANGE],height=.55)
ax.set_yticks([2,1,0],['Jac original','Jac + checked O2','Handwritten'],fontsize=17)
ax.set_xlim(0,2450);ax.set_xlabel('Actual kernel time (µs)',fontsize=15)
ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
for y,v in zip([2,1,0],values):ax.text(v+32,y,f'{v:,.3f}',va='center',fontsize=17)
text(f,'2.113 ms → 0.534 ms → 0.0205 ms',y=.17,size=27,width=90)
save(f)

f=page('What the remaining gap tells us','Interpretation','Compiler quality and graph execution strategy both deserve attention.',source='codegen/ABLATIONS.md; codegen/ablation-profile/verified-kernels.json')
text(f,'Established: scalar-state promotion removes local-memory accesses and nearly reproduces O2’s speedup.',y=.72,size=22,width=92)
text(f,'After O2: generic FIFO traversal, CSR lookups, dispatch and checks still execute. Restricted chain controls run faster on regular layouts.',y=.53,size=22,width=92)
text(f,'Those controls change the execution contract and compiler. The remaining 26× gap is a whole-implementation comparison.',y=.33,size=22,width=92)
text(f,'Cache, coalescing and occupancy attribution remains open: this study has timing traces and codegen evidence; hardware counters were unavailable.',y=.14,size=17,width=115,color=MUTED)
save(f)

f=page('Evidence and reproducibility','Data / artifacts','Source commit e476272e4 • scripts/gpu_walker/handwritten_matmul/')
table(f,['Evidence','Validation'],[
 ['Primary profiler run','11,560 launches matched; 9,600 measured'],
 ['Supplementary ablation run','43,350 launches matched; 36,000 measured'],
 ['Direct GPU correctness','13 fixtures × 3 checked variants = 39 passes'],
 ['Named-cursor CPU / JIT suite','15 tests passed'],
],bbox=(.055,.31,.89,.40),size=20,widths=[.43,.57])
text(f,'REPORT.md • primary/comparison.csv • codegen/ABLATIONS.md',y=.23,size=18,width=115)
text(f,'reproduce_codegen.sh rebuilds variants, profiles execution and validates results. This deck checks source hashes and primary table values when built.',y=.14,size=17,width=115,color=MUTED)
save(f)
pdf.close()
paths=['primary/comparison.json','codegen/codegen.json','codegen/paired-profile/verified-kernels.json','codegen/status-validation.json','codegen/ABLATIONS.md','REPORT.md']
(OUT/'sources.json').write_text(json.dumps({'measurement_commit':'e476272e42fd71c1a15319da42d4d38d23c2795a','files':[{'path':str((DATA/p).relative_to(ROOT)),'sha256':hashlib.sha256((DATA/p).read_bytes()).hexdigest()} for p in paths]},indent=2)+'\n')
print(f'Built {number} slides: {OUT / "jac-gpu-matmul.pdf"}')
