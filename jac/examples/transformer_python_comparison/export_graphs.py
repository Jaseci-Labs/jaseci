"""Rebuild inspection artifacts from actual graphs/configs in saved validation."""
import json
from pathlib import Path
import torch
from weights import Config, make_tensors
from imperative import Transformer
from explicit_fx import ExplicitTransformer


def main():
    directory = Path(__file__).parent / 'results'
    report = json.loads((directory / 'validation_cpu.json').read_text())
    for label, case in report['cases'].items():
        config = Config(**case['config'])
        dtype = getattr(torch, case['dtype'].removeprefix('torch.'))
        model = Transformer(config, make_tensors(config, dtype=dtype))
        source = torch.zeros(case['shape'][0], dtype=torch.int64)
        target = torch.zeros(case['shape'][1], dtype=torch.int64)
        direct = ExplicitTransformer(config, source, target, model.bindings(), capture=True)
        assert direct.export(directory, label) == case['counts']
        if case['output_only']:
            plain = ExplicitTransformer(config, source, target, model.bindings())
            assert plain.export(directory, 'output_only') == case['output_only']['counts']
    print('PASS: FX/DOT/spec exports rebuilt from actual graphs; counts match validation')


if __name__ == '__main__':
    main()
