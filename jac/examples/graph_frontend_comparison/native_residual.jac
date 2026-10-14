import torch;
import fixtures;
import native_validation;
import os;
edge TensorEdge { has port: str; }
edge Seed {}
node Graph {}
node Value {
    has name: str, value: any = None, box: dict[str, any] = {};
    def ready -> bool { return "a" in self.box and "b" in self.box; }
    def calc -> any { return self.value; }
}
node Input(Value) { override def ready -> bool { return True; } }
node Weight(Input) {}
node MatMul(Value) { override def calc -> any { return self.box["a"] @ self.box["b"]; } }
node Add(Value) { override def calc -> any { return self.box["a"] + self.box["b"]; } }
node ReLU(Value) {
    override def ready -> bool { return "x" in self.box; }
    override def calc -> any { return torch.relu(self.box["x"]); }
}
node Output(Add) {}
walker Run {
    has trace: list[str] = [], output: any = None;
    can start with Graph entry { visit [->:Seed:->]; }
    can step with Value entry {
        here.value = here.calc(); self.trace.append(here.name);
        if isinstance(here, Output) { self.output = here.value; }
        for e in [edge ->:TensorEdge:->] {
            dst = e.__jac__.target.archetype;
            assert isinstance(dst, Value);
            dst.box[e.port] = here.value;
            if dst.ready() { visit dst; }
        }
    }
}
# Native graph construction; no library builder.
def run -> any {
    v = fixtures.tensors(); g = Graph();
    x = Input(name="x", value=v["x"]); w = Weight(name="w", value=v["w"]);
    h = MatMul(name="h"); r = ReLU(name="r"); y = Output(name="y");
    g +>: Seed() :+> x; g +>: Seed() :+> w;
    x +>: TensorEdge(port="a") :+> h; w +>: TensorEdge(port="b") :+> h;
    h +>: TensorEdge(port="x") :+> r;
    h +>: TensorEdge(port="b") :+> y; r +>: TensorEdge(port="a") :+> y;
    return g spawn Run();
}
with entry { native_validation.main("residual", run, os.path.dirname(__file__)); }
