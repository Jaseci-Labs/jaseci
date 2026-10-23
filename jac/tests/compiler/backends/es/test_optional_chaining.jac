"""Null-safe trailers (`?.`, `?[...]`) keep their short-circuit in emitted JavaScript."""

import json;
import shutil;
import from jaclang.compiler.passes.execution { run_walker }
import from jaclang.compiler.driver.program { JacProgram }
import from jaclang.compiler.driver.compile_options { CompileOptions }
import from jaclang.compiler.backends.es.esast_gen_pass { EsastGenPass }
import from jaclang.compiler.passes.type_checker_pass { TypeCheckPass }
import from jaclang.compiler.driver.pass_driver { run_pass }
import from tests.compiler.backends.es.codegen_helpers { run_js_module }

glob OPTIONAL_SRC = """
obj Box {
    has inner: Box | None = None;
    has n: int = 0;
    def get -> int { return self.n; }
}
glob hits: list[int] = [];
def bump(x: any) -> any { hits.append(1); return x; }
def attr(x: any) -> any { return x?.a; }
def chain(x: any) -> any { return x?.a?.b; }
def index(x: any) -> any { return x?[0]; }
def index_var(x: any, i: int) -> any { return x?[i]; }
def slice_of(x: any) -> any { return x?[1:2]; }
def call(x: any) -> any { return x?.f(); }
def method(b: Box | None) -> any { return b?.get(); }
def upper(s: str | None) -> any { return s?.upper(); }
def typed_chain(b: Box | None) -> any { return b?.inner?.n; }
def once(x: any, i: int) -> any { return bump(x)?[i]; }
def subtle -> any { return globalThis.crypto?.subtle; }
def fields(details: any, envelope: any) -> any {
    return [details.error?.message, envelope.data?.identities];
}
def store(x: any) { x?.a = 1; }
""";

def compile_client(source: str) -> str {
    program = JacProgram();
    module = program.compile(
        "optional_chaining.jac",
        use_str=source,
        options=CompileOptions(force_codespace="client", no_cgen=True)
    );
    run_pass(TypeCheckPass, module, program);
    run_walker(EsastGenPass, module=module, prog=program);
    assert not program.errors_had , "\n".join(
        str(error) for error in program.errors_had
    );
    return module.gen.js;
}

test "optional chaining on any-typed values emits JavaScript optional chains" {
    js = compile_client(OPTIONAL_SRC);
    for expected in [
        "return x?.a;",
        "return x?.a?.b;",
        "return x?.[0];",
        "return x?.slice(1, 2);",
        "return x?.f();",
        "return b?.inner?.n;",
        "return globalThis.crypto?.subtle;",
        "details.error?.message",
        "envelope.data?.identities"
    ] {
        assert expected in js , f"missing {expected!r} in:\n{js}";
    }
    # JavaScript rejects an optional chain as an assignment target.
    assert "x.a = 1;" in js , js;
}

test "reading through a missing value yields undefined instead of throwing" {
    if not shutil.which("node") {
        testskip("node not on PATH");
    }
    js = compile_client(OPTIONAL_SRC);
    probe = """
const u = (v) => v === undefined;
console.log(JSON.stringify([
    u(attr(null)), u(attr(undefined)), attr({a: 1}),
    u(chain(null)), u(chain({})), chain({a: {b: 2}}),
    u(index(null)), index([5]),
    u(index_var(null, 0)), index_var([5, 6], 1),
    u(slice_of(null)), slice_of([1, 2, 3]),
    u(call(null)), call({f: () => 7}),
    u(method(null)), method(new Box({n: 4})),
    u(upper(null)), upper("ab"),
    u(typed_chain(null)), u(typed_chain(new Box())),
    typed_chain(new Box({inner: new Box({n: 9})})),
    u(once(null, 0)), once([3], 0), hits.length,
    u(fields({}, {})[0]), u(fields({}, {})[1])
]));
""";
    result = run_js_module(js + "\n" + probe, timeout=10.0);
    assert result.returncode == 0 , result.stderr + "\n" + js;
    assert json.loads(result.stdout.strip())
        == [
            True,
            True,
            1,
            True,
            True,
            2,
            True,
            5,
            True,
            6,
            True,
            [2],
            True,
            7,
            True,
            4,
            True,
            "AB",
            True,
            True,
            9,
            True,
            3,
            2,
            True,
            True
        ] , result.stdout + "\n" + js;
}

glob AWAITED_SRC = """
glob seen: list[int] = [];
def recv(x: any) -> any { seen.append(1); return x; }
async def key() -> int { return 1; }
async def word() -> str { return ","; }
async def num() -> int { return 3; }
def total(a: int, b: int = 0, c: int = 0) -> int { return a + b + c; }
async def awaited_index(x: any) -> any { return recv(x)?[await key()]; }
async def awaited_split(s: str | None) -> any { return recv(s)?.split(await word()); }
async def awaited_callee(x: any) -> any { return recv(x)?[await key()](await num()); }
async def awaited_kwargs(kw: dict[str, int]) -> int {
    return total(await num(), **kw, **kw);
}
""";

test "awaited reads inside a null-safe guard stay in their async scope" {
    js = compile_client(AWAITED_SRC);
    assert "(__jac_opt =>" not in js , js;
    assert "await (async __jac_opt =>" in js , js;
    assert "await (async __jac_kwargs =>" in js , js;
}

test "awaited reads inside a null-safe guard evaluate the receiver once" {
    if not shutil.which("node") {
        testskip("node not on PATH");
    }
    js = compile_client(AWAITED_SRC);
    probe = """
const u = (v) => v === undefined;
const out = [
    u(await awaited_index(null)), await awaited_index([5, 6]), seen.length,
    u(await awaited_split(null)), await awaited_split("a,b"), seen.length,
    await awaited_callee([0, (n) => n * 2]), seen.length,
    await awaited_kwargs({b: 1, c: 2})
];
console.log(JSON.stringify(out));
""";
    result = run_js_module(js + "\n" + probe, timeout=10.0);
    assert result.returncode == 0 , result.stderr + "\n" + js;
    assert json.loads(result.stdout.strip())
        == [True, 6, 2, True, ["a", "b"], 4, 6, 5, 6] , result.stdout + "\n" + js;
}
