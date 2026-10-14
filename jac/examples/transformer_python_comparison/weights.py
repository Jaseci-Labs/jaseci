"""Shared deterministic tensors/configuration, with no forward or FX construction."""
from dataclasses import asdict, dataclass
import math
import torch


@dataclass(frozen=True)
class Config:
    dimension: int = 8
    heads: int = 2
    hidden: int = 16
    vocabulary: int = 13
    capacity: int = 64
    epsilon: float = 1e-5

    def __post_init__(self):
        if self.heads < 2 or self.dimension <= 0 or self.dimension % self.heads:
            raise ValueError('dimension must be positive/divisible by heads >= 2')
        if self.hidden <= 0 or self.vocabulary <= 2 or self.capacity <= 0 or self.epsilon <= 0:
            raise ValueError('invalid configuration')

    def as_dict(self):
        return asdict(self)


def make_tensors(config, device='cpu', dtype=torch.float64, seed=1729):
    """Linear weights use nn.Linear's [out, in] convention. No hidden RNG use."""
    c = config
    generator = torch.Generator(device='cpu').manual_seed(seed)
    tensors = {}

    def weight(name, shape, divisor):
        tensors[name] = torch.randn(shape, generator=generator, dtype=torch.float64) / math.sqrt(divisor)

    def linear(name, din, dout):
        weight(name + '.weight', (dout, din), din)
        tensors[name + '.bias'] = torch.zeros(dout, dtype=torch.float64)

    weight('enc_embed.weight', (c.vocabulary, c.dimension), c.vocabulary)
    weight('dec_embed.weight', (c.vocabulary, c.dimension), c.vocabulary)
    for attention in ('enc_attn', 'dec_attn', 'cross_attn'):
        for projection in ('q', 'k', 'v', 'output'):
            linear(attention + '.' + projection, c.dimension, c.dimension)
    for ffn in ('enc_ffn', 'dec_ffn'):
        linear(ffn + '.up', c.dimension, c.hidden)
        linear(ffn + '.output', c.hidden, c.dimension)
    for norm in ('enc_norm1', 'enc_norm2', 'dec_norm1', 'dec_norm2', 'dec_norm3'):
        tensors[norm + '.weight'] = torch.ones(c.dimension, dtype=torch.float64)
        tensors[norm + '.bias'] = torch.zeros(c.dimension, dtype=torch.float64)
    linear('projection', c.dimension, c.vocabulary)
    rows = torch.arange(c.capacity, dtype=torch.float64).unsqueeze(1)
    columns = torch.arange(c.dimension, dtype=torch.float64)
    angles = rows * torch.pow(10000., -2 * torch.floor(columns / 2) / c.dimension)
    tensors['position_table'] = torch.where((columns.to(torch.int64) % 2 == 0).unsqueeze(0), angles.sin(), angles.cos())
    return {name: value.to(device=device, dtype=dtype) for name, value in tensors.items()}
