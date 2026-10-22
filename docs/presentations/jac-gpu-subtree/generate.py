#!/usr/bin/env python3
"""Generate an English white/sans-serif PDF from verified subtree GPU evidence."""
import hashlib
import json
import os
from pathlib import Path
import textwrap
os.environ.setdefault('MPLCONFIGDIR','/tmp/jac-subtree-deck-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
DATA=ROOT/'scripts/gpu_walker/subtree_query/validation/20261021'
read=lambda path:json.loads(path.read_text())
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
comparison=read(DATA/'primary/comparison.json')
for path,digest in comparison['sources_sha256'].items():assert sha(DATA/path)==digest,path
rows=comparison['rows'];by_id={x['id']:x for x in rows}
verified=read(DATA/'profile/verified.json');aux=read(DATA/'ablation-profile/verified.json')
lookup={(x['case'],x['arm']):x for x in verified['summaries']}
aux_lookup={(x['case'],x['arm']):x for x in aux['summaries']}
for row in rows:
    for key,arm in [('original_us','Jac original'),('optimized_us','Jac O2'),('handwritten_us','CUDA checked')]:
        assert row[key]==lookup[(row['id'],arm)]['median_us']
manifest=read(DATA/'inputs.json');run=read(DATA/'profile/results.json');correct=read(DATA/'correctness.json')
assert verified['results_sha256']==sha(DATA/'profile/results.json')
assert verified['sqlite_sha256']==sha(DATA/'profile/trace.sqlite')
assert aux['results_sha256']==sha(DATA/'ablation-profile/results.json')
assert aux['sqlite_sha256']==sha(DATA/'ablation-profile/trace.sqlite')
assert correct['status']=='PASS'
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42})
INK,MUTED,BLUE,TEAL,ORANGE='#16263f','#59677b','#2563eb','#078477','#bd681c'
pdf=PdfPages(OUT/'jac-gpu-subtree.pdf');pdf.infodict()['Title']='Jac GPU: Batched Subtree Queries'
page_count=0

def page(title,section,subtitle='',source='primary/comparison.json · profile/verified.json'):
    global page_count
    page_count+=1
    fig=plt.figure(figsize=(16,9),facecolor='white')
    fig.text(.055,.95,'JAC ON GPU  /  '+section.upper(),fontsize=11,weight='bold',color=TEAL)
    fig.text(.055,.875,title,fontsize=27,weight='bold',color=INK)
    fig.text(.055,.81,subtitle,fontsize=15,color=MUTED)
    fig.text(.055,.032,'2026-10-21/22  •  '+source,fontsize=8,color=MUTED)
    fig.text(.95,.032,str(page_count),ha='right',fontsize=10,color=MUTED)
    return fig

def text(fig,s,y=.72,size=21,width=98,x=.06,color=INK):
    fig.text(x,y,textwrap.fill(s,width,break_long_words=False),fontsize=size,va='top',color=color,linespacing=1.45)

def table(fig,heads,contents,bbox=(.055,.22,.89,.50),size=18,widths=None):
    ax=fig.add_axes([0,0,1,1]);ax.axis('off')
    t=ax.table(cellText=contents,colLabels=heads,cellLoc='left',colLoc='left',bbox=bbox,colWidths=widths)
    t.auto_set_font_size(False);t.set_fontsize(size)
    for (r,c),cell in t.get_celld().items():
        cell.set_edgecolor('#dce4ee');cell.set_linewidth(.7)
        cell.set_facecolor('#e8eff8' if r==0 else '#f5f7fb' if r%2 else 'white')
        cell.set_text_props(color=INK,weight='bold' if r==0 else 'normal')

def save(fig):pdf.savefig(fig);plt.close(fig)

f=page('Batched subtree queries on Jac GPU','Research question','Production CSR Jac • checked LLVM O2 Jac • handwritten checked CUDA')
text(f,'How does general graph traversal compare when every implementation executes the same subtree queries?',size=30,width=59)
text(f,'17 workloads cover balanced and irregular trees, varied query batches, negative values, leaves and thresholds.',y=.44,size=23,width=85)
text(f,'RTX 3090 • shared GPU context • resident actual kernel durations',y=.20,size=18,color=MUTED)
save(f)

f=page('One query: root, threshold and five results','Semantics','Traverse the root and every descendant; match amount ≥ threshold.',source='jac/examples/gpu/subtree_query.jac · correctness.json')
ax=f.add_axes([.06,.33,.38,.39]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
positions=[(.5,.78),(.19,.25),(.81,.25)]
for child in [1,2]:ax.annotate('',xy=(positions[child][0],positions[child][1]+.13),xytext=(positions[0][0],positions[0][1]-.13),arrowprops={'arrowstyle':'->','color':MUTED,'lw':2})
for (x,y),label in zip(positions,['amount 2\nalert false','amount −4\nalert true','amount 7\nalert true']):
    ax.add_patch(FancyBboxPatch((x-.16,y-.11),.32,.22,boxstyle='round,pad=.018',facecolor='#eaf1fb',edgecolor='#aebed4'))
    ax.text(x,y,label,ha='center',va='center',fontsize=16,color=INK)
table(f,['Query','count / sum / alert / visited'],[
    ['root; threshold 0','2 / 9 / true / 3'],['left leaf; threshold −4','1 / −4 / true / 1'],['right leaf; threshold 8','0 / 0 / false / 1']],bbox=(.47,.36,.475,.32),size=16,widths=[.42,.58])
text(f,'The alert flag combines qualifying nodes. The threshold is retained as the fifth state field. Every query owns its count, sum, flag, visited count and FIFO.',y=.22,size=20,width=104)
save(f)

f=page('Three implementations share one packed graph','Implementations','Fixed production pack_walkers discovery order; identical CSR, roots and thresholds.')
table(f,['Group','Compilation and traversal'],[
    ['Original Jac','Production CSR LLVM → existing target-machine codegen'],
    ['Checked optimized Jac','Same raw LLVM → standard LLVM O2 → target codegen'],
    ['Handwritten CUDA','Fixed checked per-query CSR FIFO kernel; same predicates'],
],bbox=(.055,.33,.89,.38),size=19,widths=[.31,.69])
text(f,'All primary kernels use one thread per query, 128-thread blocks, slot-major FIFO scratch, five outputs and full status checks.',y=.23,size=20,width=103)
text(f,'The checked O2 compilation path is experimental. Each arm has private outputs/scratch and shared immutable input pointers.',y=.12,size=17,width=117,color=MUTED)
save(f)

f=page('Full workloads fit a measured VRAM budget','Protocol','Exact live FIFO capacity is computed over every query.',source='inputs.json · memory-probe.json · profile/results.json')
visits=sum(x['total_node_visits'] for x in manifest['cases'])
peak=max(x['planned_device_bytes'] for x in read(DATA/'ablation-profile/results.json')['cases'])
free=manifest['memory_probe']['memory_after_context']['free']
table(f,['Factor','Sweep / evidence'],[
    ['Tree shape','Binary, ternary, quaternary, ragged, chain, irregular'],
    ['Tree size / depth','37…16,383 nodes; depth 5…2,047'],
    ['Query batches','1…1,024; root, mixed subtree and leaf queries'],
    ['Complete CPU-checked work',f'{visits:,} node visits across 17 workloads'],
    ['Free VRAM / peak 8-arm plan',f'{free/1e6:.2f} MB / {peak/1e6:.2f} MB'],
],bbox=(.055,.29,.89,.44),size=19,widths=[.37,.63])
text(f,'Scratch bytes = queries × exact FIFO capacity × 8 per arm. The GPU is shared with Ollama, which held approximately 23,462 MiB.',y=.18,size=18,width=112,color=MUTED)
save(f)

for chunk,title in [(rows[:9],'Three-way result: balanced and ragged trees'),(rows[9:],'Three-way result: chain, irregular and controls')]:
    f=page(title,'Primary data','Median actual kernel duration in µs; all three columns use one interleaved run.')
    contents=[[r['id'],*[f'{r[key]:,.3f}' for key in ['original_us','optimized_us','handwritten_us']]] for r in chunk]
    table(f,['Workload','Original Jac','Checked Jac + O2','Handwritten'],contents,bbox=(.055,.18,.89,.57),size=17,widths=[.43,.19,.20,.18])
    text(f,'120 measured kernel samples per cell • 3 warmup rounds • 15 measured rounds × 8 graph nodes • seed 928',y=.115,size=16,width=128,color=MUTED)
    save(f)

f=page('Original CSR Jac closely tracks checked CUDA','Primary interpretation','LLVM O2 usually adds latency in this sweep; both variants retain full checks.')
selected=['binary511-root32','binary4095-mixed256','irregular16383-mixed256','binary1023-root128-all','binary1023-root128-none']
ax=f.add_axes([.30,.26,.61,.44]);yy=list(range(len(selected)))
ax.barh([x+.17 for x in yy],[by_id[k]['optimized_us']/by_id[k]['original_us'] for k in selected],height=.30,color=TEAL,label='Checked Jac + O2')
ax.barh([x-.17 for x in yy],[by_id[k]['handwritten_us']/by_id[k]['original_us'] for k in selected],height=.30,color=ORANGE,label='Handwritten checked')
ax.axvline(1,color=BLUE,linestyle='--',lw=1.8,label='Original Jac = 1')
ax.set_yticks(yy,selected,fontsize=13);ax.invert_yaxis();ax.set_xlim(.9,1.16)
ax.set_xlabel('Duration / original Jac (lower is faster)',fontsize=14)
ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0);ax.legend(fontsize=12,loc='lower right')
text(f,'Irregular 16,383-node batch: 8.271 ms original → 8.939 ms O2 → 8.365 ms handwritten.',y=.16,size=21,width=107)
save(f)

f=page('This backend already uses SSA state','Compiler evidence','Single-cursor CSR lowering is inspected independently.',source='codegen/input.ll · codegen/codegen.json · driver function attributes')
table(f,['Property','Original Jac','Checked O2','Handwritten'],[
    ['LLVM allocas','0','0','CUDA source'],
    ['PTX local load / store sites','0 / 0','0 / 0','0 / 0'],
    ['Driver-JIT local bytes','0','0','0'],
    ['Driver-JIT registers','38','40','40'],
],bbox=(.055,.32,.89,.39),size=19,widths=[.43,.19,.19,.19])
text(f,'FIFO positions, pending/step counters and query states are LLVM phi values. SROA-only emits identical PTX to the production baseline.',y=.23,size=20,width=105)
text(f,'O2 changes generated code, including static global-store sites 13 → 8. Hardware attribution for its measured slowdown remains unresolved.',y=.11,size=17,width=120,color=MUTED)
save(f)

f=page('Batching and matching work change latency','Controlled workloads','Graph hashes and control identity are verified against the saved arrays.')
a=by_id['binary1023-root1'];b=by_id['binary1023-root128-all'];n=by_id['binary1023-root128-none']
table(f,['Control on the same 1,023-node tree','Visits','Original Jac (µs)'],[
    ['1 root query, threshold −1001',f"{a['total_node_visits']:,}",f"{a['original_us']:.3f}"],
    ['128 root queries, threshold −1001',f"{b['total_node_visits']:,}",f"{b['original_us']:.3f}"],
    ['128 root queries, threshold +1001',f"{n['total_node_visits']:,}",f"{n['original_us']:.3f}"],
],bbox=(.055,.35,.89,.36),size=19,widths=[.58,.19,.23])
text(f,f"128× the visits takes {b['original_us']/a['original_us']:.2f}× the latency in the all-match batch contrast.",y=.25,size=22,width=105)
text(f,'All-match and no-match queries both traverse every node. Their timing contrast includes the count, sum and alert work on qualifying nodes.',y=.12,size=18,width=115,color=MUTED)
save(f)

f=page('Controlled check and FIFO layout experiments','Supplementary data','Mixed: 4,095 nodes / 256 queries. Uniform: 1,023 nodes / 128 queries. Times in ms.',source='ablation-profile/verified.json · ablation-ordinary/results.json')
cid='binary4095-mixed256'
labels=['Checked O2','Bypass overflow','Bypass validation','Bypass both']
arms=['Jac O2','Jac O2_no_overflow','Jac O2_no_validation','Jac O2_unchecked']
values=[aux_lookup[(cid,arm)]['median_us']/1000 for arm in arms]
table(f,['LLVM check experiment','Kernel ms'],[[label,f'{value:.3f}'] for label,value in zip(labels,values)],bbox=(.055,.35,.48,.37),size=18,widths=[.76,.24])
layout_cases=['binary4095-mixed256','binary1023-root128-all']
table(f,['CUDA scratch layout','Mixed','Uniform root'],[
    ['Slot-major checked',*[f"{aux_lookup[(x,'CUDA checked')]['median_us']/1000:.3f}" for x in layout_cases]],
    ['Query-major checked',*[f"{aux_lookup[(x,'CUDA query-major')]['median_us']/1000:.3f}" for x in layout_cases]],
],bbox=(.57,.40,.375,.25),size=16,widths=[.50,.25,.25])
text(f,'Bypass variants use validated finite, bounded tree inputs. Their elapsed times compare complete generated implementations.',y=.24,size=19,width=108)
text(f,'Query-major scratch is faster for mixed queries and slower for uniform full-root batches here. Cache/coalescing/occupancy attribution remains open.',y=.11,size=17,width=119,color=MUTED)
save(f)

f=page('Correctness covers valid work and status paths','Validation','All five result fields and status are checked after every replay.',source='correctness.json · profile/verified.json · ablation-profile/verified.json')
table(f,['Evidence','Result'],[
    ['Serial Jac + independent CPU reference','17 full workloads; 632,829 query-node visits'],
    ['Direct checked GPU fixtures','17 fixtures × 4 kernels = 68 passing launches'],
    ['Primary launch name/order/grid/block audit','7,395 verified; 6,120 measured nodes'],
    ['Supplementary launch audit','19,720 verified; 16,320 measured nodes'],
    ['Existing subtree CPU/JIT suite','4 tests passed'],
],bbox=(.055,.31,.89,.42),size=18,widths=[.48,.52])
text(f,'Fixtures include values above 2^53, negative sums, overflow, private state, malformed CSR, queue/visit limits, cycles and empty roots.',y=.20,size=19,width=108)
text(f,'Output/status poisoning happens before the event interval. Error fixtures compare directly with the unmodified production LLVM JIT.',y=.10,size=17,width=120,color=MUTED)
save(f)

f=page('A graph-to-graph comparison gives a closer baseline','Findings','The measured task is generic subtree traversal over the same CSR inputs.')
text(f,'Original production CSR Jac is close to the straightforward checked handwritten kernel across this sweep.',y=.72,size=24,width=83)
text(f,'Checked LLVM O2 preserves semantics and usually adds latency here. This lowering already has zero local stack storage.',y=.52,size=23,width=88)
text(f,'Batch size, qualifying-node work and FIFO layout have measured effects. The hardware causes of remaining differences stay open.',y=.32,size=23,width=88)
text(f,'REPORT.md • primary/comparison.csv • raw traces/results • reproducible scripts and source hashes',y=.14,size=17,width=122,color=MUTED)
save(f)
pdf.close()
paths=['primary/comparison.json','profile/verified.json','profile/results.json','ablation-profile/verified.json','codegen/codegen.json','correctness.json','REPORT.md','inputs.json']
(OUT/'sources.json').write_text(json.dumps({'unit':'microseconds','primary_source_run':'profile','generator_sha256':sha(Path(__file__)),
    'sources':[{'path':str((DATA/path).relative_to(ROOT)),'sha256':sha(DATA/path)} for path in paths]},indent=2)+'\n')
print(f'Built {page_count} white/sans-serif slides: {OUT/"jac-gpu-subtree.pdf"}')
