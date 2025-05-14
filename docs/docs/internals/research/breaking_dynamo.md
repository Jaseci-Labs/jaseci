# 🧠 TorchDynamo FX Graphs: A Deep Dive
> _Exploring the internals of FX graph tracing — and the places it goes south._

Pytorch 2.0 introduced a novel framework for lowering pytorch models into accelarator hardware. The main two components of this framework is Torch Dynamo (frontend compiler) and Torch Inductor (backend compiler). On a high level, the torch dynamo genarates an fx-graph from python bytecode, which is an intermediat representation of code than can be compiled for accelarator hardware which is the compiled using the TorchInducter to produce Triton code.

In this document we explore the TorchDynamo frontend compiler and how it genarate fx-graph IR from bytecode. Some of the main research questions that we strive top answer from this exploration are,

1. Where graph breaks are applied in Dynamo?
2. Are each of these graph breaks always necessary?

## Into the Deep End

We will now go though the pipline of genarating the fx-graph through TorchDynamo using the (pytorch codebase)[https://github.com/pytorch/pytorch] and many other resorces.

The compilation process starts with ```torch.compile``` call for a defined function. In the following example we show this in action.

```python
class Model(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        y = torch.sin(x)
        z = torch.cos(x)

        # Combine and return
        return y**2 + z**2

model = Model()
compiled = torch.compile(model)
```

When this compiled model is called with input values it will produce fx-graph IR for the foward function.

