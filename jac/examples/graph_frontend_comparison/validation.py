"""Executed by cases.jac: actual Jac walker vs independent manually built FX."""
import json
from pathlib import Path
import torch
import direct_fx
import fixtures


class Counts:
    """CPU operator counts only; no timing results or CUDA profiling."""
    def __enter__(self):
        self.profiler = torch.autograd.profiler.profile(use_cpu=True, use_cuda=False)
        self.profiler.__enter__()
        return self

    def __exit__(self, *exc):
        self.profiler.__exit__(*exc)
        self.counts = {event.key: event.count for event in self.profiler.key_averages()}


def export_fx(module, path):
    text = '"""Actual direct FX export; shared scaffold is in direct_fx.py."""\nimport torch\n\n'
    text += module.code.lstrip()
    for name, child in module.named_children():
        text += '\n# Branch GraphModule: ' + name + '\n' + child.code.lstrip()
    path.write_text('\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n')


def main(linear, residual, conditional, directory):
    torch.set_num_threads(1)
    directory = Path(directory)
    values = fixtures.tensors()
    report = dict(status='passed', device='cpu', dtype='float64',
                  torch=torch.__version__, shape_x=[2, 2], shape_w_in_out=[2, 2], cases={})
    for name, jac, builder in [('linear', linear, direct_fx.linear),
                                ('residual', residual, direct_fx.residual),
                                ('cond', conditional, direct_fx.conditional)]:
        module = builder()
        assert sum(n.op == 'call_function' and n.target is direct_fx.mm
                   for n in module.graph.nodes) == 1
        torch.testing.assert_close(jac.ops['w'].value, values['w'])
        records = []
        for predicate in ([True, False, True] if name == 'cond' else [None]):
            feeds = {'x': values['x']}
            args = [values['x'], values['w']]
            h = values['x'] @ values['w']
            if name == 'linear':
                args.append(values['b']); expected = h + values['b']
                torch.testing.assert_close(jac.ops['b'].value, values['b'])
            elif name == 'residual':
                expected = h.relu() + h
            else:
                c = torch.tensor(predicate, dtype=torch.bool)
                feeds['c'] = c; args.append(c)
                expected = h + values['x'] if predicate else h - values['x']
            if jac.plan is None:
                jac.prepare(feeds)  # metadata analysis is outside numerical counts
            with Counts() as jc:
                run = jac.run(feeds, capture=['h'])
            with torch.inference_mode(), Counts() as fc:
                actual = module(*args)
            torch.testing.assert_close(run.output, expected, atol=0, rtol=0)
            torch.testing.assert_close(actual, expected, atol=0, rtol=0)
            torch.testing.assert_close(run.captured['h'], h, atol=0, rtol=0)
            assert run.trace.count('h') == 1
            assert jc.counts.get('aten::mm') == fc.counts.get('aten::mm') == 1
            if name == 'cond':
                selected, excluded = ('t', 'f') if predicate else ('f', 't')
                assert selected in run.trace and excluded not in run.trace
                assert fc.counts.get('aten::add', 0) == int(predicate)
                assert fc.counts.get('aten::sub', 0) == int(not predicate)
                assert 'h' in jac.plan['conditional']['pre']
            records.append(dict(predicate=predicate, jac_trace=run.trace,
                                jac_mm_calls=jc.counts['aten::mm'],
                                fx_mm_calls=fc.counts['aten::mm'],
                                fx_add_calls=fc.counts.get('aten::add', 0),
                                fx_sub_calls=fc.counts.get('aten::sub', 0),
                                max_abs_error=float((run.output - actual).abs().max()),
                                output=actual.tolist()))
        report['cases'][name] = records
        jac.export_dot(str(directory / (name + '_jac.dot')))
        export_fx(module, directory / (name + '_fx.py'))
    (directory / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: Jac walker / direct FX, three cases, Cond true/false/true')
    print('W [in,out]; each shared MatMul executes once; max error 0')
