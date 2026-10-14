"""Three aligned presentation excerpts; runnable example sources are unchanged."""
import os
import textwrap
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/jac-slides-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).parent


def draw_graph(ax, case):
    """Semantic dependencies, not a literal export of either frontend IR."""
    from matplotlib.transforms import Affine2D
    class ShiftedAxes:
        def __getattr__(self, name):
            fn = getattr(ax_original, name)
            if name in ('text', 'plot', 'annotate'):
                def call(*args, **kwargs):
                    kwargs['transform'] = Affine2D().translate(8, 0) + ax_original.transData
                    if name == 'annotate':
                        kwargs.pop('transform', None)
                        kwargs['xy'] = (kwargs['xy'][0]+8, kwargs['xy'][1])
                        kwargs['xytext'] = (kwargs['xytext'][0]+8, kwargs['xytext'][1])
                    return fn(*args, **kwargs)
                return call
            if name == 'add_patch':
                def patch(p):
                    p.set_transform(Affine2D().translate(8, 0) + ax_original.transData)
                    return ax_original.add_patch(p)
                return patch
            return fn
    ax_original = ax
    ax = ShiftedAxes()
    ink, teal, muted = '#17243b', '#078477', '#53647b'
    ax.plot([19.8, 19.8], [2.4, 9.35], color='#dbe3ef')
    ax.text(20.3, 9.15, 'Computation graph', fontsize=21, weight='bold', color=teal)
    if case == 1:
        nodes = {'x': (21,8), 'w': (24,8), 'h': (22.5,6.4), 'b': (24.7,5), 'y': (22.5,4)}
        labels = {'h':'h = MatMul', 'y':'y = Add'}
        links = [('x','h'),('w','h'),('h','y'),('b','y')]
    elif case == 2:
        nodes = {'x': (21,8), 'w': (24,8), 'h': (22.5,6.4), 'r': (21.5,4.9), 'y': (23,3.3)}
        labels = {'h':'h = MatMul','r':'r = ReLU','y':'y = Add'}
        links = [('x','h'),('w','h'),('h','r'),('r','y'),('h','y')]
    else:
        nodes = {'x': (21,8.3), 'w': (24.5,8.3), 'h': (22.7,7),
                 't': (21.5,5.4), 'f': (24.5,5.4), 'c': (20.7,3.8), 'y': (23.3,3.5)}
        labels = {'h':'h = MatMul','t':'t = h + x','f':'f = h - x','y':'y = Cond'}
        links = [('x','h'),('w','h'),('h','t'),('h','f'),('x','t'),('x','f'),('t','y'),('f','y'),('c','y')]
        for center in (21.5,24.5):
            ax.add_patch(FancyBboxPatch((center-1.23,4.8),2.46,1.2,boxstyle='round,pad=.04',facecolor='#fff9ed',edgecolor='#c76b16',linestyle='--'))
        ax.text(21.5,6.13,'true branch',ha='center',fontsize=13,color='#a65c16')
        ax.text(24.5,6.13,'false branch',ha='center',fontsize=13,color='#a65c16')
    for src,dst in links:
        x,y=nodes[src];u,v=nodes[dst];dx,dy=u-x,v-y
        scale=min(.92/abs(dx) if dx else float('inf'),.34/abs(dy) if dy else float('inf'))
        lazy=case==3 and src in ('t','f') and dst=='y'
        ax.annotate('',xy=(u-dx*scale,v-dy*scale),xytext=(x+dx*scale,y+dy*scale),arrowprops=dict(arrowstyle='->',color='#c76b16' if lazy else muted,lw=1.6,linestyle='--' if lazy else '-', connectionstyle='arc3,rad=-0.35' if case==3 and src=='x' and dst=='f' else 'arc3,rad=0'))
    for key,(x,y) in nodes.items():
        ax.add_patch(FancyBboxPatch((x-.87,y-.29),1.74,.58,boxstyle='round,pad=.05',facecolor='#eef5f4',edgecolor=teal))
        ax.text(x,y,labels.get(key,key),fontsize=14,ha='center',va='center',color=ink)
    note = 'Shared h is computed once.' if case!=3 else 'Only one branch executes.\nDashed arrows: lazy result selection.'
    ax.text(20.3,2.65,note,fontsize=14,color=muted,linespacing=1.4)
    ax.text(20.3,1.95,'Semantic diagram; not a literal\nJac or FX node export.',fontsize=12,color=muted)


def discussion_slide(pdf, title, subtitle, points, footer):
    fig = plt.figure(figsize=(26.5, 11.25), facecolor='white')
    ax = fig.add_axes([0,0,1,1]); ax.set(xlim=(0,26.5), ylim=(0,11.25)); ax.axis('off')
    ax.text(.8,10.35,title,fontsize=34,weight='bold',color='#17243b')
    ax.text(.8,9.55,subtitle,fontsize=24,color='#078477')
    for i,(heading,body) in enumerate(points):
        y=8.45-i*2.15
        ax.text(.9,y,heading,fontsize=27,weight='bold',color='#17243b',va='top')
        ax.text(.9,y-.6,'\n'.join(textwrap.wrap(body,125)),fontsize=23,color='#53647b',va='top',linespacing=1.35)
    ax.text(.8,.45,footer,fontsize=15,color='#53647b')
    pdf.savefig(fig); plt.close(fig)


def static_graph_slide(pdf):
    fig=plt.figure(figsize=(26.5,11.25),facecolor='white')
    ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,26.5),ylim=(0,11.25));ax.axis('off')
    ax.text(.8,10.35,'FX and ONNX can be graph-first representations',fontsize=34,weight='bold',color='#17243b')
    ax.text(.8,9.55,'A graph can be constructed directly; it does not have to be recovered from Python execution.',fontsize=24,color='#078477')
    nodes={'Input A':(3.5,7.6),'Input B':(3.5,5.8),'Input C':(3.5,4),
           'OP 1':(9,6.7),'OP 2':(14.5,7.5),'OP 3':(20,5.5),'Output':(24,5.5)}
    links=[('Input A','OP 1'),('Input B','OP 1'),('OP 1','OP 2'),('OP 1','OP 3'),('Input C','OP 3'),('OP 2','OP 3'),('OP 3','Output')]
    for src,dst in links:
        x,y=nodes[src];u,v=nodes[dst];dx,dy=u-x,v-y
        scale=min(1.35/abs(dx) if dx else float('inf'),.43/abs(dy) if dy else float('inf'))
        ax.annotate('',xy=(u-dx*scale,v-dy*scale),xytext=(x+dx*scale,y+dy*scale),arrowprops=dict(arrowstyle='->',lw=2,color='#53647b',connectionstyle='arc3,rad=0.13' if src=='Input C' else 'arc3,rad=0'))
    for label,(x,y) in nodes.items():
        ax.add_patch(FancyBboxPatch((x-1.3,y-.38),2.6,.76,boxstyle='round,pad=.05',facecolor='#eef5f4' if label.startswith('OP') else '#f3f6fa',edgecolor='#078477'))
        ax.text(x,y,label,fontsize=24,ha='center',va='center',color='#17243b')
    ax.text(.9,2.65,'Explicit inputs, operation nodes, dependencies and shared intermediate values can all be represented in FX and ONNX.',fontsize=23,color='#17243b')
    ax.text(.9,1.65,'Question: what does Jac add when constructing and using this same static graph?',fontsize=25,weight='bold',color='#078477')
    ax.text(.8,.45,'Abstract dependency graph; no code shown. Static structure does not imply constant input values or fully fixed tensor shapes.',fontsize=15,color='#53647b')
    pdf.savefig(fig);plt.close(fig)


def build():
    ink, muted, blue, teal = '#17243b', '#53647b', '#2563eb', '#078477'
    cases = [
        ('Linear', 'y = x @ w + b', [
            ('1  Multiply', 'h = MatMul();\nx +>: A() :+> h;\nw +>: B() :+> h;', 'h = g.call_function(mm, (x, w))'),
            ('2  Add bias', 'y = Add();\nh +>: A() :+> y;\nb +>: B() :+> y;', 'y = g.call_function(add, (h, b))'),
        ]),
        ('Shared computation + residual', 'h = x @ w; y = relu(h) + h', [
            ('1  Multiply once', 'h = MatMul();\nx +>: A() :+> h;\nw +>: B() :+> h;', 'h = g.call_function(mm, (x, w))'),
            ('2  ReLU', 'r = ReLU();\nh +>: X() :+> r;', 'r = g.call_function(relu, (h,))'),
            ('3  Residual add', 'y = Add();\nr +>: A() :+> y;\nh +>: B() :+> y;', 'y = g.call_function(add, (r, h))'),
        ]),
        ('Conditional: same result, different construction', 'h = x @ w; y = h + x if c else h - x', [
            ('1  Shared multiply', 'h = MatMul();\nx +>: A() :+> h;\nw +>: B() :+> h;', 'h = g.call_function(mm, (x, w))'),
            ('2  Branch bodies', 't = Add(); f = Subtract();\nh +>: A() :+> t;\nx +>: B() :+> t;\nh +>: A() :+> f;\nx +>: B() :+> f;', 't, f = cond_modules(g, root, add, sub)\n# t(h,x) -> clone(h+x)\n# f(h,x) -> clone(h-x)'),
            ('3  Select + join', 'gate +>: Then() :+> t;\ngate +>: Else() :+> f;\nt +>: X() :+> y;\nf +>: X() :+> y;', 'r = g.call_function(cond, (c, t, f, (h, x)))\ny = g.call_function(getitem, (r, 0))'),
        ]),
    ]
    # The excerpts below use native typed-edge syntax, but simplify custom
    # constructors/edge names for explanation. They are not executable exports.
    with PdfPages(OUT/'jac-vs-python-fx.pdf') as pdf:
        pdf.infodict()['Title'] = 'From Two Roads to the GPU to a concrete Jac versus FX discussion'
        discussion_slide(pdf, 'Connecting to Two Roads to the GPU',
            'Shared premise: explicit computation semantics can reduce graph-capture work.', [
            ('The Python route', 'Python model -> capture and specialization -> computation graph -> optimization and code generation.'),
            ('The graph-first route', 'Explicit graph -> optimization and code generation. Fusion, layouts and memory planning remain backend work.'),
            ('Our question', 'Direct FX and ONNX construction are also graph-first. What useful role would a Jac frontend add?')],
            'Context: professor-provided Two Roads to the GPU, pp. 1, 4-6. Paraphrase and discussion framing, not a new performance result.')
        static_graph_slide(pdf)
        onnx_rows = [
            ['nh = N("MatMul", ["x", "w"], ["h"])',
             'ny = N("Add", ["h", "b"], ["y"])'],
            ['nh = N("MatMul", ["x", "w"], ["h"])',
             'nr = N("Relu", ["h"], ["r"])',
             'ny = N("Add", ["r", "h"], ["y"])'],
            ['nh = N("MatMul", ["x", "w"], ["h"])',
             'tg = G([N("Add", ["h", "x"], ["t"])],\n       "then", [], [t_info])\nfg = G([N("Sub", ["h", "x"], ["f"])],\n       "else", [], [f_info])',
             'ny = N("If", ["c"], ["y"],\n       then_branch=tg, else_branch=fg)'],
        ]
        for n, (title, equation, rows) in enumerate(cases, 1):
            fig = plt.figure(figsize=(34.5, 11.25), facecolor='white')
            ax = fig.add_axes([0, 0, 1, 1]); ax.set(xlim=(0,34.5), ylim=(0,11.25)); ax.axis('off')
            ax.text(.6, 10.55, f'{n}. {title}', fontsize=27, weight='bold', color=ink)
            ax.text(.6, 9.95, equation, fontsize=22, color=muted)
            ax.text(3.1, 9.15, 'Jac: explicit nodes + edges', fontsize=22, weight='bold', color=teal)
            ax.text(11.05, 9.15, 'Python: FX node construction', fontsize=22, weight='bold', color=blue)
            ax.text(20.15, 9.15, 'Python: ONNX construction', fontsize=22, weight='bold', color='#a65c16')
            top = 8.75
            row_h = 2.15
            for i, (label, jac, fx) in enumerate(rows):
                y = top-i*row_h
                ax.text(.6, y-.35, label, fontsize=17, color=ink, weight='bold', va='top')
                for x, width, code in [(3.05,7.45,jac),(11,8.35,fx),(20.1,7.1,onnx_rows[n-1][i])]:
                    ax.add_patch(FancyBboxPatch((x,y-1.95),width,1.8,boxstyle='round,pad=.1',facecolor='#f3f6fa',edgecolor='#dbe3ef'))
                    size=16 if n==3 or x>19 else 20
                    ax.text(x+.2,y-.4,code,fontsize=size,family='DejaVu Sans Mono',va='top',color=ink,linespacing=1.2)
            ax.text(.6, 2.05, 'Aligned by operation semantics, not by source lines. Presentation excerpts only; runnable sources are unchanged.',fontsize=15,color=ink)
            ax.text(.6, 1.5, 'Jac shorthand: A/B/X stand for typed input-port edges. Names, values, node/walker definitions and execution are omitted.',fontsize=14,color=muted)
            if n==3:
                ax.text(.6,1.0,'Cond is not a one-to-one node mapping: Jac uses a gate + control edges + output join; FX uses two branch modules.',fontsize=14,color=muted)
                ax.text(.6,.55,'mm = torch.ops.aten.mm.default. Gate setup / wrapping omitted; custom Jac types are not builtins.',fontsize=14,color=muted)
            else:
                ax.text(.6,1.0,'FX aliases: mm = torch.ops.aten.mm.default; add/relu are ATen operators. Input setup and execution are omitted.',fontsize=14,color=muted)
                ax.text(.6,.55,'Full sources and verification: jac/examples/graph_frontend_comparison/  |  No timing or usability claim.',fontsize=14,color=muted)
            ax.text(20.1,1.5,'N = onnx.helper.make_node',fontsize=14,color=muted)
            ax.text(20.1,1.05,'G = onnx.helper.make_graph; types/setup omitted.',fontsize=14,color=muted)
            if n == 3:
                ax.text(20.1,.6,'Outer h/x captured; only one branch runs.',fontsize=14,color=muted)
            else:
                ax.text(20.1,.6,'ONNX snippets: API examples, not runtime-tested.',fontsize=14,color=muted)
            draw_graph(ax, n)
            pdf.savefig(fig); plt.close(fig)
        discussion_slide(pdf, 'What the examples show so far',
            'All three representations express the math; graph-first benefits are not unique to Jac.', [
            ('Linear and shared computation', 'FX handles, ONNX value names and native Jac edges encode dependencies and shared intermediate values.'),
            ('Conditional selection', 'The native Jac example handwrites gate, routing and readiness behavior. FX uses Cond with branch GraphModules; ONNX uses If with branch GraphProto attributes.'),
            ('Current limitation', 'The code does not establish that Jac is simpler. These custom native node/walker types are not automatically lowered to FX.')],
            'These are observations about the shown implementations, not a proof that either language is universally better.')
        discussion_slide(pdf, 'Research goal to confirm',
            'Which contribution should this frontend aim to demonstrate?', [
            ('Programming experience', 'A better way to express an actual user task: compare against Python helpers and torch.cond, with equal abstraction levels.'),
            ('Semantic guarantees', 'Specify additional shape, effect or control-flow guarantees, and show what errors or manual reasoning they eliminate.'),
            ('Optimization or performance', 'Identify information or analysis missing from the baseline, then measure its effect. The same FX graph alone predicts no speed gain.')],
            'Question for discussion: If Jac generates the same FX graph, what evidence would make the extra frontend worth using?')
    print(OUT/'jac-vs-python-fx.pdf')


if __name__ == '__main__':
    build()
