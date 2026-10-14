import torch;
import fixtures;
import native_validation;
import os;
edge TensorEdge { has port: str; }
edge Seed {}
node Graph {}
node Value {
    has name: str, value: any = None, box: dict[str, any] = {}, enabled: bool = True;
    def ready -> bool { return "a" in self.box and "b" in self.box; }
    def calc -> any { return self.value; }
}
node Input(Value) { override def ready -> bool { return True; } }
node Weight(Input) {}
node MatMul(Value) { override def calc -> any { return self.box["a"] @ self.box["b"]; } }
node Add(Value) { override def calc -> any { return self.box["a"] + self.box["b"]; } }
edge Then {}
edge Else {}
node Subtract(Value) { override def calc -> any { return self.box["a"] - self.box["b"]; } }
node Select(Value) {
    override def ready -> bool { return all([p in self.box for p in ["c", "h", "x"]]); }
}
node Output(Value) {
    override def ready -> bool { return "x" in self.box; }
    override def calc -> any { return self.box["x"].contiguous().clone(); }
}
walker Run {
    has trace: list[str] = [], output: any = None;
    can start with Graph entry { visit [->:Seed:->]; }
    can step with Value entry {
        self.trace.append(here.name);
        if isinstance(here, Select) {
            chosen = [->:Then:->] if bool(here.box["c"].item()) else [->:Else:->];
            for branch in chosen {
                assert isinstance(branch, Value);
                branch.enabled = True;
                if branch.ready() { visit branch; }
            }
            return;
        }
        here.value = here.calc();
        if isinstance(here, Output) { self.output = here.value; }
        for e in [edge ->:TensorEdge:->] {
            dst = e.__jac__.target.archetype;
            assert isinstance(dst, Value);
            dst.box[e.port] = here.value;
            if dst.enabled and dst.ready() { visit dst; }
        }
    }
}
# Native graph construction; data and control edges are explicit.
def run(predicate: bool) -> any {
    v = fixtures.tensors(); g = Graph();
    x = Input(name="x", value=v["x"]); w = Weight(name="w", value=v["w"]);
    c = Input(name="c", value=torch.tensor(predicate, dtype=torch.bool));
    h = MatMul(name="h"); gate = Select(name="select"); y = Output(name="y");
    t = Add(name="t", enabled=False); f = Subtract(name="f", enabled=False);
    g +>: Seed() :+> x; g +>: Seed() :+> w; g +>: Seed() :+> c;
    x +>: TensorEdge(port="a") :+> h; w +>: TensorEdge(port="b") :+> h;
    c +>: TensorEdge(port="c") :+> gate;
    h +>: TensorEdge(port="h") :+> gate; x +>: TensorEdge(port="x") :+> gate;
    h +>: TensorEdge(port="a") :+> t; x +>: TensorEdge(port="b") :+> t;
    h +>: TensorEdge(port="a") :+> f; x +>: TensorEdge(port="b") :+> f;
    gate +>: Then() :+> t; gate +>: Else() :+> f;
    t +>: TensorEdge(port="x") :+> y; f +>: TensorEdge(port="x") :+> y;
    return g spawn Run();
}
with entry { native_validation.main("cond", run, os.path.dirname(__file__)); }
