"""Test actual native walkers independently against direct FX and Torch math."""
import json
from pathlib import Path
import torch
import fixtures
import direct_fx
from validation import Counts


def main(case, run_native, directory):
    torch.set_num_threads(1)
    v = fixtures.tensors()
    module = dict(linear=direct_fx.linear, residual=direct_fx.residual,
                  cond=direct_fx.conditional)[case]()
    records = []
    for predicate in ([True, False, True] if case == 'cond' else [None]):
        args = [v['x'], v['w']]
        h = v['x'] @ v['w']
        if case == 'linear':
            args.append(v['b']); expected = h + v['b']
        elif case == 'residual':
            expected = h.relu() + h
        else:
            args.append(torch.tensor(predicate, dtype=torch.bool))
            expected = h + v['x'] if predicate else h - v['x']
        with torch.inference_mode(), Counts() as jc:
            run = run_native(predicate) if case == 'cond' else run_native()
        with torch.inference_mode(), Counts() as fc:
            result = module(*args)
        torch.testing.assert_close(run.output, expected, atol=0, rtol=0)
        torch.testing.assert_close(result, expected, atol=0, rtol=0)
        assert run.trace.count('h') == 1
        assert jc.counts.get('aten::mm') == fc.counts.get('aten::mm') == 1
        if case == 'cond':
            chosen, excluded = ('t', 'f') if predicate else ('f', 't')
            assert chosen in run.trace and excluded not in run.trace
            assert jc.counts.get('aten::add', 0) == fc.counts.get('aten::add', 0) == int(predicate)
            assert jc.counts.get('aten::sub', 0) == fc.counts.get('aten::sub', 0) == int(not predicate)
        records.append(dict(predicate=predicate, native_trace=run.trace,
                            native_mm_calls=jc.counts['aten::mm'], fx_mm_calls=fc.counts['aten::mm'],
                            native_add_calls=jc.counts.get('aten::add', 0), native_sub_calls=jc.counts.get('aten::sub', 0),
                            fx_add_calls=fc.counts.get('aten::add', 0), fx_sub_calls=fc.counts.get('aten::sub', 0),
                            max_abs_error=float((run.output-result).abs().max()), output=result.tolist()))
    path = Path(directory) / ('validation_native_' + case + '.json')
    path.write_text(json.dumps(dict(case=case, status='passed', device='cpu', dtype='float64',
                                    graph_lifetime='fresh graph per invocation', records=records), indent=2)+'\n')
    print('PASS native', case, 'CPU float64; exact FX parity; shared MatMul once')
