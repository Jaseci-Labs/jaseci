"""Run ordinary nn.Module, manually built FX and direct Inductor on shared inputs."""
import os
from pathlib import Path
os.environ.setdefault('TORCHINDUCTOR_CACHE_DIR', '/tmp/transformer-python-comparison-inductor')
os.environ.setdefault('TORCHINDUCTOR_COMPILE_THREADS', '1')
os.environ.setdefault('MAX_JOBS', '1')
import torch
from weights import Config, make_tensors
from imperative import Transformer
from explicit_fx import ExplicitTransformer
from audit import forbid_frontend_capture


def main():
    torch.set_num_threads(1)
    config = Config()
    model = Transformer(config, make_tensors(config))
    source = torch.tensor([3, 4, 5, 2], dtype=torch.int64)
    # Teacher forcing for labels [6,7,2]: [BOS=1,6,7].
    target = torch.tensor([1, 6, 7], dtype=torch.int64)
    with torch.inference_mode():
        expected = model(source, target)
    with forbid_frontend_capture() as audit:
        direct = ExplicitTransformer(config, source, target, model.bindings())
        eager, _ = direct.eager(source, target, model.bindings())
        direct.compile(source, target, model.bindings())
        compiled, _ = direct(source, target, model.bindings())
        torch.testing.assert_close(eager, expected, atol=2e-11, rtol=2e-10)
        torch.testing.assert_close(compiled, expected, atol=2e-11, rtol=2e-10)
    counts = direct.export(Path(__file__).parent / 'results', 'demo')
    print('probabilities:', tuple(compiled.shape))
    print('maximum absolute error:', float((compiled - expected).abs().max()))
    print('compiler entry:', direct.compiler_entry, '; frontend capture calls:', audit['calls'])
    print('FX node counts:', counts['node_counts'])
    print('Random initialized weights demonstrate computation, not generation quality.')


if __name__ == '__main__':
    main()
