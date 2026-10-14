"""CPU/CUDA correctness comparison; no benchmark and no Jac imports."""
import argparse
import json
import os
from pathlib import Path
import platform

os.environ.setdefault('TORCHINDUCTOR_CACHE_DIR', '/tmp/transformer-python-comparison-inductor')
os.environ.setdefault('TORCHINDUCTOR_COMPILE_THREADS', '1')
os.environ.setdefault('MAX_JOBS', '1')

import torch
from audit import forbid_frontend_capture
from explicit_fx import ExplicitTransformer
from imperative import Transformer
from weights import Config, make_tensors
from preserve import check as preservation_check

HERE = Path(__file__).resolve().parent


def error(actual, expected):
    if actual.dtype == torch.bool:
        assert torch.equal(actual, expected)
        return 0.
    assert torch.equal(torch.isfinite(actual), torch.isfinite(expected))
    assert torch.equal(torch.isposinf(actual), torch.isposinf(expected))
    assert torch.equal(torch.isneginf(actual), torch.isneginf(expected))
    finite = torch.isfinite(expected)
    return float((actual[finite] - expected[finite]).abs().max()) if bool(finite.any()) else 0.


def compare(actual, expected, dtype):
    tol = dict(atol=2e-11, rtol=2e-10) if dtype == torch.float64 else dict(atol=3e-5, rtol=3e-4)
    torch.testing.assert_close(actual, expected, **tol)
    return error(actual, expected)


def reject(fn, expected):
    try:
        fn()
    except ValueError as exc:
        assert expected in str(exc), str(exc)
        return str(exc)
    raise AssertionError('expected rejection: ' + expected)


def inputs(config, source_length, target_length, device):
    source = ((torch.arange(source_length, device=device) + 3) % config.vocabulary).to(torch.int64)
    labels = ((torch.arange(target_length, device=device) + 6) % config.vocabulary).to(torch.int64)
    # Teacher-forced decoder input = BOS followed by all labels except last.
    target = torch.cat((torch.ones(1, dtype=torch.int64, device=device), labels[:-1]))
    return source, target, labels


def run_case(label, config, shape, dtype, device):
    source, target, labels = inputs(config, *shape, device)
    tensors = make_tensors(config, device, dtype)
    model = Transformer(config, tensors)
    assert len(dict(model.named_parameters())) == 46
    # Both implementations consume these same tensors; no hidden/copied FX weights.
    for name, value in model.bindings().items():
        assert value.data_ptr() == tensors[name].data_ptr()
    with torch.inference_mode():
        expected, reference = model(source, target, return_intermediates=True)
    with forbid_frontend_capture() as audit:
        direct = ExplicitTransformer(config, source, target, model.bindings(), capture=True)
        assert not list(direct.module.parameters()) and not list(direct.module.buffers())
        assert all(n.op in ('placeholder', 'call_function', 'output') for n in direct.module.graph.nodes)
        assert all(isinstance(n.target, torch._ops.OpOverload) for n in direct.module.graph.nodes if n.op == 'call_function')
        eager, eager_values = direct.eager(source, target, model.bindings())
        direct.compile(source, target, model.bindings())
        compiled, compiled_values = direct(source, target, model.bindings())
        assert set(reference) == set(eager_values) == set(compiled_values)
        intermediate_errors = {name: dict(fx=compare(eager_values[name], value, dtype),
                                          inductor=compare(compiled_values[name], value, dtype))
                               for name, value in reference.items()}
        compare(eager, expected, dtype); compare(compiled, expected, dtype)
        assert torch.isfinite(compiled).all()
        compare(compiled.sum(-1), torch.ones(shape[1], dtype=dtype, device=device), dtype)
        mask = compiled_values['dec_attn.mask']
        assert torch.equal(mask, torch.ones(shape[1], shape[1], device=device, dtype=torch.bool).triu(1))
        assert torch.equal(compiled_values['dec_attn.probabilities'].masked_select(mask),
                           torch.zeros_like(compiled_values['dec_attn.probabilities'].masked_select(mask)))
        for prefix, main, skip in [('enc_norm1', 'enc_attn.output', 'enc_pos'),
                                   ('enc_norm2', 'enc_ffn.output', 'enc_norm1'),
                                   ('dec_norm1', 'dec_attn.output', 'dec_pos'),
                                   ('dec_norm2', 'cross_attn.output', 'dec_norm1'),
                                   ('dec_norm3', 'dec_ffn.output', 'dec_norm2')]:
            compare(compiled_values[prefix + '.residual'], compiled_values[main] + compiled_values[skip], dtype)
        repeated_errors = []
        for index in range(3):
            changed_source = source.clone(); changed_source[-1] = (changed_source[-1] + index) % config.vocabulary
            changed_target = target.clone(); changed_target[-1] = (changed_target[-1] + index) % config.vocabulary
            with torch.inference_mode():
                ref = model(changed_source, changed_target)
            actual, _ = direct(changed_source, changed_target, model.bindings())
            repeated_errors.append(compare(actual, ref, dtype))
        repeated, _ = direct(source, target, model.bindings())
        compare(repeated, compiled, dtype)
        # Causal isolation: changing the final decoder input cannot change earlier outputs.
        changed_target = target.clone(); changed_target[-1] = (changed_target[-1] + 1) % config.vocabulary
        future, future_values = direct(source, changed_target, model.bindings())
        if target.numel() > 1:
            compare(future[:-1], compiled[:-1], dtype)
            compare(future_values['dec_attn.q'][:-1], compiled_values['dec_attn.q'][:-1], dtype)
        changed_source = source.clone(); changed_source[-1] = (changed_source[-1] + 1) % config.vocabulary
        influenced, influenced_values = direct(changed_source, target, model.bindings())
        memory_delta = error(influenced_values['enc_norm2'], compiled_values['enc_norm2'])
        cross_delta = error(influenced_values['cross_attn.k'], compiled_values['cross_attn.k'])
        encoder_delta = error(influenced, compiled)
        assert memory_delta > 1e-8 and cross_delta > 1e-8 and encoder_delta > 1e-8
        # Inputs are arguments: existing compiled code must observe new weight values.
        weight_deltas = {}
        for name in ('enc_embed.weight', 'enc_attn.q.weight', 'dec_attn.k.weight', 'cross_attn.v.weight',
                     'enc_ffn.up.weight', 'dec_ffn.output.weight', 'enc_norm1.weight', 'dec_norm3.bias',
                     'projection.weight', 'projection.bias', 'position_table'):
            old = model.bindings()[name]
            perturb = torch.sin(torch.arange(old.numel(), device=device, dtype=dtype).reshape(old.shape) + .3) * .025
            replacement = old + perturb
            if name == 'position_table':
                model.position_table = replacement
            else:
                parent, leaf = name.rsplit('.', 1)
                model.get_submodule(parent)._parameters[leaf] = torch.nn.Parameter(replacement, requires_grad=False)
            with torch.inference_mode():
                ref, ref_values = model(source, target, return_intermediates=True)
            actual, changed_values = direct(source, target, model.bindings())
            compare(actual, ref, dtype)
            for checkpoint in ref_values:
                compare(changed_values[checkpoint], ref_values[checkpoint], dtype)
            delta = error(actual, compiled)
            checkpoint = name.rsplit('.', 1)[0] if name != 'position_table' else 'enc_pos'
            local_delta = error(changed_values[checkpoint], compiled_values[checkpoint])
            assert local_delta > 1e-8, name
            invariant = target.numel() == 1 and name == 'dec_attn.k.weight'
            if invariant:
                compare(actual, compiled, dtype)  # one-key attention probability is always one
            else:
                assert delta > 1e-10, name
            weight_deltas[name] = dict(output_delta=delta, checkpoint=checkpoint,
                                      checkpoint_delta=local_delta, expected_output_invariance=invariant)
            if name == 'position_table':
                model.position_table = old
            else:
                model.get_submodule(parent)._parameters[leaf] = old
        with torch.no_grad():
            model.projection.bias.add_(torch.arange(config.vocabulary, dtype=dtype, device=device) * .01)
        with torch.inference_mode():
            ref = model(source, target)
        mutated, _ = direct(source, target, model.bindings())
        compare(mutated, ref, dtype)
        assert error(mutated, compiled) > 1e-8
        with torch.no_grad():
            model.projection.bias.sub_(torch.arange(config.vocabulary, dtype=dtype, device=device) * .01)
        # Static signatures guard the direct backend callable rather than Dynamo guards.
        bad_shape = reject(lambda: direct(torch.cat((source, source[:1])), target, model.bindings()), 'metadata changed')
        bad_dtype = reject(lambda: direct(source.to(torch.int32), target, model.bindings()), 'int64')
        bad_weights = model.bindings(); bad_weights['projection.weight'] = bad_weights['projection.weight'][:, :-1]
        bad_weight_shape = reject(lambda: direct(source, target, bad_weights), 'metadata changed')
        bad_bindings = model.bindings(); del bad_bindings['projection.bias']
        missing_weight = reject(lambda: direct(source, target, bad_bindings), 'weight names changed')
        counts = direct.export(HERE / 'results', label)
        # Also compile a true output-only graph: captures change optimization boundaries.
        output_only = None
        if label == 'small_float64_4x3':
            plain = ExplicitTransformer(config, source, target, model.bindings(), capture=False)
            plain.compile(source, target, model.bindings())
            actual, captured = plain(source, target, model.bindings())
            assert not captured
            output_only = dict(max_abs_error=compare(actual, expected, dtype),
                               counts=plain.export(HERE / 'results', 'output_only'))
    return dict(status='passed', config=config.as_dict(), shape=list(shape), dtype=str(dtype), device=str(device),
                compiler_entry=direct.compiler_entry, fallback=None, frontend_audit=audit, counts=counts,
                checked_intermediates=len(reference), intermediate_errors=intermediate_errors,
                final_errors=dict(fx=error(eager, expected), inductor=error(compiled, expected)),
                repeated_changed_input_errors=repeated_errors, shifted_target=target.cpu().tolist(), labels=labels.cpu().tolist(),
                causal_mask='passed', future_isolation='passed' if target.numel() > 1 else 'vacuous_length_one',
                residual_joins=5, encoder_influence=dict(memory=memory_delta, cross_keys=cross_delta, output=encoder_delta),
                replaced_weights=weight_deltas, in_place_mutation='passed', output_only=output_only,
                metadata_guards=dict(input_shape=bad_shape, input_dtype=bad_dtype, weight_shape=bad_weight_shape, missing_weight=missing_weight))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--device', default='cpu', choices=('cpu', 'cuda:0'))
    args = ap.parse_args()
    if args.device.startswith('cuda') and not torch.cuda.is_available():
        raise SystemExit('CUDA unavailable in this interpreter; CPU-only Torch build cannot validate CUDA')
    torch.set_num_threads(1)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    report = dict(environment=dict(python=platform.python_version(), torch=torch.__version__, device=args.device,
                                   cpu_threads=1, tf32=False, compiler_cache=os.environ['TORCHINDUCTOR_CACHE_DIR']),
                  cases={}, compiler_entry='torch._inductor.compile_fx.compile_fx', dynamo_frontend_capture=False,
                  fallback=None, cuda_status='not_run: host RTX3090 occupied by Ollama; isolated validation venv uses CPU-only torch' if args.device == 'cpu' else 'passed')
    cases = [('small_float64_4x3', Config(), (4, 3), torch.float64),
             ('small_float64_2x1', Config(), (2, 1), torch.float64),
             ('small_float32_4x3', Config(), (4, 3), torch.float32),
             ('medium_float32_7x5', Config(dimension=32, heads=4, hidden=64, vocabulary=31), (7, 5), torch.float32)]
    for label, config, shape, dtype in cases:
        print('validate', label, args.device, flush=True)
        report['cases'][label] = run_case(label, config, shape, dtype, args.device)
    report['preservation'] = preservation_check()
    report['status'] = 'passed'
    path = HERE / 'results' / ('validation_' + args.device.replace(':', '_') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS', path)


if __name__ == '__main__':
    main()
