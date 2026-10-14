"""Version 2: construct an ATen FX graph directly; no Jac/tracing/Dynamo capture.

Python helpers below only BUILD nodes. Numerical execution is GraphModule or
Inductor's callable, never a custom operation-dispatch interpreter.
"""
from collections import Counter
import copy
from pathlib import Path
import json
import torch
from torch import fx
from weights import Config

aten = torch.ops.aten


class GraphBuilder:
    def __init__(self, config: Config, source_length, target_length, bindings, capture=False):
        self.config = config
        self.source_length, self.target_length = source_length, target_length
        if not 0 < source_length <= config.capacity or not 0 < target_length <= config.capacity:
            raise ValueError('sequence lengths must fit positional capacity')
        self.graph = fx.Graph()
        self.values = {}
        self.source = self.graph.placeholder('source')
        self.target = self.graph.placeholder('target')
        self.weight_names = tuple(sorted(bindings))
        self.weights = {}
        for index, name in enumerate(self.weight_names):
            node = self.graph.placeholder('weight_' + str(index))
            node.meta['weight_name'] = name
            self.weights[name] = node
        self.device = next(iter(bindings.values())).device
        self.capture = capture

    def op(self, name, target, *args, **kwargs):
        node = self.graph.call_function(target, args, kwargs)
        node.meta['expression_name'] = name
        return node

    def save(self, name, value):
        self.values[name] = value
        return value

    def linear(self, prefix, x):
        wt = self.op(prefix + '.weight_transpose', aten.t.default, self.weights[prefix + '.weight'])
        mm = self.op(prefix + '.matmul', aten.mm.default, x, wt)
        return self.save(prefix, self.op(prefix, aten.add.Tensor, mm, self.weights[prefix + '.bias']))

    def embedding(self, prefix, tokens):
        selected = self.op(prefix + '.gather', aten.index_select.default, self.weights[prefix + '.weight'], 0, tokens)
        return self.save(prefix, self.op(prefix, aten.mul.Scalar, selected, self.config.dimension ** .5))

    def positional(self, prefix, embedding, length):
        positions = self.op(prefix + '.positions', aten.slice.Tensor, self.weights['position_table'], 0, 0, length)
        return self.save(prefix, self.op(prefix, aten.add.Tensor, embedding, positions))

    def attention(self, prefix, query, memory, query_length, memory_length, causal=False):
        c = self.config
        width = c.dimension // c.heads
        heads = {}
        for letter, producer, length in (('q', query, query_length), ('k', memory, memory_length), ('v', memory, memory_length)):
            projection = self.linear(prefix + '.' + letter, producer)
            reshaped = self.op(prefix + '.' + letter + '.reshape', aten.reshape.default, projection, [length, c.heads, width])
            heads[letter] = self.op(prefix + '.' + letter + '.heads', aten.transpose.int, reshaped, 0, 1)
        kt = self.op(prefix + '.k_transpose', aten.transpose.int, heads['k'], -2, -1)
        raw = self.op(prefix + '.score_matmul', aten.bmm.default, heads['q'], kt)
        scores = self.save(prefix + '.score', self.op(prefix + '.score', aten.div.Scalar, raw, width ** .5))
        if causal:
            full = self.op(prefix + '.mask_full', aten.ones.default, [query_length, query_length], dtype=torch.bool, device=self.device)
            mask = self.save(prefix + '.mask', self.op(prefix + '.mask', aten.triu.default, full, 1))
            scores = self.save(prefix + '.masked', self.op(prefix + '.masked', aten.masked_fill.Scalar, scores, mask, -float('inf')))
        probabilities = self.save(prefix + '.probabilities', self.op(prefix + '.probabilities', aten._softmax.default, scores, -1, False))
        context = self.save(prefix + '.context', self.op(prefix + '.context', aten.bmm.default, probabilities, heads['v']))
        transposed = self.op(prefix + '.context_transpose', aten.transpose.int, context, 0, 1)
        contiguous = self.op(prefix + '.context_contiguous', aten.contiguous.default, transposed)
        joined = self.op(prefix + '.joined', aten.reshape.default, contiguous, [query_length, c.dimension])
        # Match the public attention-output checkpoint name in the ordinary model.
        return self.linear(prefix + '.output', joined)

    def norm(self, prefix, x, residual):
        joined = self.save(prefix + '.residual', self.op(prefix + '.residual', aten.add.Tensor, x, residual))
        mean = self.op(prefix + '.mean', aten.mean.dim, joined, [-1], True)
        centered = self.op(prefix + '.center', aten.sub.Tensor, joined, mean)
        squared = self.op(prefix + '.square', aten.square.default, centered)
        variance = self.op(prefix + '.variance', aten.mean.dim, squared, [-1], True)
        stable = self.op(prefix + '.stable', aten.add.Scalar, variance, self.config.epsilon)
        inverse = self.op(prefix + '.rsqrt', aten.rsqrt.default, stable)
        normalized = self.op(prefix + '.normalized', aten.mul.Tensor, centered, inverse)
        scaled = self.op(prefix + '.scaled', aten.mul.Tensor, normalized, self.weights[prefix + '.weight'])
        return self.save(prefix, self.op(prefix, aten.add.Tensor, scaled, self.weights[prefix + '.bias']))

    def ffn(self, prefix, x):
        up = self.linear(prefix + '.up', x)
        activated = self.save(prefix + '.relu', self.op(prefix + '.relu', aten.relu.default, up))
        return self.linear(prefix + '.output', activated)

    def build(self):
        s, t = self.source_length, self.target_length
        ep = self.positional('enc_pos', self.embedding('enc_embed', self.source), s)
        dp = self.positional('dec_pos', self.embedding('dec_embed', self.target), t)
        ea = self.attention('enc_attn', ep, ep, s, s)
        en1 = self.norm('enc_norm1', ea, ep)
        memory = self.norm('enc_norm2', self.ffn('enc_ffn', en1), en1)
        da = self.attention('dec_attn', dp, dp, t, t, causal=True)
        dn1 = self.norm('dec_norm1', da, dp)
        ca = self.attention('cross_attn', dn1, memory, t, s)
        dn2 = self.norm('dec_norm2', ca, dn1)
        dn3 = self.norm('dec_norm3', self.ffn('dec_ffn', dn2), dn2)
        logits = self.linear('projection', dn3)
        probabilities = self.save('probabilities', self.op('probabilities', aten._softmax.default, logits, -1, False))
        self.capture_names = tuple(self.values) if self.capture else ()
        self.graph.output((probabilities, *(self.values[n] for n in self.capture_names)))
        self.graph.lint()
        return fx.GraphModule(torch.nn.Module(), self.graph, 'ExplicitTransformerATen')


def tensor_spec(tensor):
    return dict(shape=list(tensor.shape), stride=list(tensor.stride()), dtype=str(tensor.dtype),
                device=str(tensor.device), requires_grad=tensor.requires_grad)


class ExplicitTransformer:
    """Fixed-shape manually constructed graph, with explicit runtime weight inputs."""
    def __init__(self, config, source, target, bindings, *, capture=False):
        self.config = config
        self.builder = GraphBuilder(config, source.numel(), target.numel(), bindings, capture)
        self.module = self.builder.build()
        self.weight_names = self.builder.weight_names
        self.capture_names = self.builder.capture_names
        examples = self.arguments(source, target, bindings)
        self.signature = tuple(tensor_spec(t) for t in examples)
        self.compiled = None
        self.compiler_entry = None

    def arguments(self, source, target, bindings):
        if set(bindings) != set(self.weight_names):
            raise ValueError('weight names changed')
        if source.dtype != torch.int64 or target.dtype != torch.int64 or source.ndim != 1 or target.ndim != 1:
            raise ValueError('inputs must be rank-one int64 token tensors')
        return [source, target, *(bindings[name] for name in self.weight_names)]

    def checked_arguments(self, source, target, bindings):
        args = self.arguments(source, target, bindings)
        if tuple(tensor_spec(t) for t in args) != self.signature:
            raise ValueError('shape/stride/dtype/device/grad metadata changed: rebuild and recompile')
        return args

    def eager(self, source, target, bindings):
        with torch.inference_mode():
            result = self.module(*self.checked_arguments(source, target, bindings))
        return result[0], dict(zip(self.capture_names, result[1:]))

    def compile(self, source, target, bindings):
        # Internal/version-sensitive direct backend entry. There is NO fallback.
        from torch._inductor.compile_fx import compile_fx
        args = self.checked_arguments(source, target, bindings)
        with torch.inference_mode():
            self.compiled = compile_fx(copy.deepcopy(self.module), args, config_patches={'compile_threads': 1, 'triton.cudagraphs': False})
        self.compiler_entry = 'torch._inductor.compile_fx.compile_fx'
        return self

    def __call__(self, source, target, bindings):
        if self.compiled is None:
            raise RuntimeError('call compile() first')
        with torch.inference_mode():
            result = self.compiled(*self.checked_arguments(source, target, bindings))
        return result[0], dict(zip(self.capture_names, result[1:]))

    def export(self, directory, stem):
        directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
        code = '"""Actual manually constructed FX forward; weights are explicit arguments."""\nimport torch\nfrom math import inf\n\n' + self.module.code.lstrip()
        (directory / (stem + '_fx.py')).write_text('\n'.join(line.rstrip() for line in code.splitlines()).rstrip() + '\n')
        lines = ['digraph ExplicitTransformer {', 'rankdir=LR;']
        for node in self.module.graph.nodes:
            label = node.name + '\\n' + str(node.target)
            if 'weight_name' in node.meta:
                label += '\\n' + node.meta['weight_name']
            if 'expression_name' in node.meta:
                label += '\\n' + node.meta['expression_name']
            lines.append(json.dumps(node.name) + ' [label=' + json.dumps(label) + '];')
            for parent in node.all_input_nodes:
                lines.append(json.dumps(parent.name) + ' -> ' + json.dumps(node.name) + ';')
        (directory / (stem + '.dot')).write_text('\n'.join(lines + ['}']) + '\n')
        spec = dict(config=self.config.as_dict(), source_length=self.builder.source_length,
                    target_length=self.builder.target_length, capture_names=list(self.capture_names),
                    weights=[dict(argument='weight_' + str(i), name=name, metadata=self.signature[i + 2])
                             for i, name in enumerate(self.weight_names)],
                    expressions={node.name: node.meta['expression_name'] for node in self.module.graph.nodes
                                 if 'expression_name' in node.meta})
        (directory / (stem + '_spec.json')).write_text(json.dumps(spec, indent=2) + '\n')
        counts = Counter(n.op for n in self.module.graph.nodes)
        ops = Counter(str(n.target) for n in self.module.graph.nodes if n.op == 'call_function')
        return dict(node_counts=dict(counts), aten_operations=dict(sorted(ops.items())),
                    weight_inputs=len(self.weight_names), captures=len(self.capture_names))
