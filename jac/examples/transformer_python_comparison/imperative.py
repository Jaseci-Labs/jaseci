"""Version 1: ordinary PyTorch nn.Module forward; no FX or compilation code."""
import math
import torch
from torch import nn
from weights import Config


def save(values, name, tensor):
    if values is not None:
        values[name] = tensor
    return tensor


class Attention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.heads = config.heads
        self.width = config.dimension // config.heads
        self.q = nn.Linear(config.dimension, config.dimension)
        self.k = nn.Linear(config.dimension, config.dimension)
        self.v = nn.Linear(config.dimension, config.dimension)
        self.output = nn.Linear(config.dimension, config.dimension)

    def forward(self, query, memory, *, causal=False, values=None, prefix=''):
        q = save(values, prefix + '.q', self.q(query))
        k = save(values, prefix + '.k', self.k(memory))
        v = save(values, prefix + '.v', self.v(memory))
        q = q.reshape(-1, self.heads, self.width).transpose(0, 1)
        k = k.reshape(-1, self.heads, self.width).transpose(0, 1)
        v = v.reshape(-1, self.heads, self.width).transpose(0, 1)
        scores = save(values, prefix + '.score', (q @ k.transpose(-2, -1)) / math.sqrt(self.width))
        if causal:
            mask = torch.ones((query.shape[0], query.shape[0]), dtype=torch.bool, device=query.device).triu(1)
            save(values, prefix + '.mask', mask)
            scores = save(values, prefix + '.masked', scores.masked_fill(mask, -math.inf))
        probabilities = save(values, prefix + '.probabilities', scores.softmax(-1))
        context = save(values, prefix + '.context', probabilities @ v)
        joined = context.transpose(0, 1).contiguous().reshape(query.shape[0], -1)
        return save(values, prefix + '.output', self.output(joined))


class FeedForward(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.up = nn.Linear(config.dimension, config.hidden)
        self.output = nn.Linear(config.hidden, config.dimension)
        self.relu = nn.ReLU()

    def forward(self, x, *, values=None, prefix=''):
        hidden = save(values, prefix + '.up', self.up(x))
        activated = save(values, prefix + '.relu', self.relu(hidden))
        return save(values, prefix + '.output', self.output(activated))


class Transformer(nn.Module):
    """One postnorm encoder + decoder, unbatched sequences, no dropout/training."""
    def __init__(self, config: Config, tensors):
        super().__init__()
        c = self.config = config
        self.enc_embed = nn.Embedding(c.vocabulary, c.dimension)
        self.dec_embed = nn.Embedding(c.vocabulary, c.dimension)
        self.register_buffer('position_table', tensors['position_table'])
        self.enc_attn = Attention(c)
        self.dec_attn = Attention(c)
        self.cross_attn = Attention(c)
        self.enc_ffn = FeedForward(c)
        self.dec_ffn = FeedForward(c)
        self.enc_norm1 = nn.LayerNorm(c.dimension, eps=c.epsilon)
        self.enc_norm2 = nn.LayerNorm(c.dimension, eps=c.epsilon)
        self.dec_norm1 = nn.LayerNorm(c.dimension, eps=c.epsilon)
        self.dec_norm2 = nn.LayerNorm(c.dimension, eps=c.epsilon)
        self.dec_norm3 = nn.LayerNorm(c.dimension, eps=c.epsilon)
        self.projection = nn.Linear(c.dimension, c.vocabulary)
        # Bind storage directly, rather than silently maintaining a copied model.
        expected = dict(self.named_parameters())
        if set(tensors) != set(expected) | {'position_table'}:
            raise ValueError('weight names do not match model')
        for name, old in expected.items():
            value = tensors[name]
            if value.shape != old.shape:
                raise ValueError('weight shape mismatch: ' + name)
            parent_name, leaf = name.rsplit('.', 1)
            self.get_submodule(parent_name)._parameters[leaf] = nn.Parameter(value, requires_grad=False)
        self.eval()

    def bindings(self):
        return {**dict(self.named_parameters()), 'position_table': self.position_table}

    def forward(self, source, target, *, return_intermediates=False):
        c = self.config
        values = {} if return_intermediates else None
        enc_embed = save(values, 'enc_embed', self.enc_embed(source) * math.sqrt(c.dimension))
        enc_pos = save(values, 'enc_pos', enc_embed + self.position_table[:source.shape[0]])
        enc_attn = self.enc_attn(enc_pos, enc_pos, values=values, prefix='enc_attn')
        enc_join = save(values, 'enc_norm1.residual', enc_attn + enc_pos)
        enc_norm1 = save(values, 'enc_norm1', self.enc_norm1(enc_join))
        enc_ffn = self.enc_ffn(enc_norm1, values=values, prefix='enc_ffn')
        enc_join2 = save(values, 'enc_norm2.residual', enc_ffn + enc_norm1)
        memory = save(values, 'enc_norm2', self.enc_norm2(enc_join2))
        dec_embed = save(values, 'dec_embed', self.dec_embed(target) * math.sqrt(c.dimension))
        dec_pos = save(values, 'dec_pos', dec_embed + self.position_table[:target.shape[0]])
        dec_attn = self.dec_attn(dec_pos, dec_pos, causal=True, values=values, prefix='dec_attn')
        dec_join = save(values, 'dec_norm1.residual', dec_attn + dec_pos)
        dec_norm1 = save(values, 'dec_norm1', self.dec_norm1(dec_join))
        cross = self.cross_attn(dec_norm1, memory, values=values, prefix='cross_attn')
        cross_join = save(values, 'dec_norm2.residual', cross + dec_norm1)
        dec_norm2 = save(values, 'dec_norm2', self.dec_norm2(cross_join))
        dec_ffn = self.dec_ffn(dec_norm2, values=values, prefix='dec_ffn')
        dec_join2 = save(values, 'dec_norm3.residual', dec_ffn + dec_norm2)
        dec_norm3 = save(values, 'dec_norm3', self.dec_norm3(dec_join2))
        logits = save(values, 'projection', self.projection(dec_norm3))
        probabilities = save(values, 'probabilities', logits.softmax(-1))
        return (probabilities, values) if return_intermediates else probabilities
