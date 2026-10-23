"""Operators and keyword calls keep their meaning in emitted JavaScript."""

import json;
import shutil;
import from jaclang.compiler.passes.execution { run_walker }
import from jaclang.compiler.driver.program { JacProgram }
import from jaclang.compiler.driver.compile_options { CompileOptions }
import from jaclang.compiler.backends.es.esast_gen_pass { EsastGenPass }
import from jaclang.compiler.passes.type_checker_pass { TypeCheckPass }
import from jaclang.compiler.driver.pass_driver { run_pass }
import from tests.compiler.backends.es.codegen_helpers { run_js_module }

def compile_client(source: str) -> str {
    program = JacProgram();
    module = program.compile(
        "operator_call_lowering.jac",
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

def run_probe(js: str, probe: str) -> list[object] {
    result = run_js_module(js + "\n" + probe, timeout=10.0);
    assert result.returncode == 0 , result.stderr + "\n" + js;
    return json.loads(result.stdout.strip());
}

glob UNTYPED_OPS_SRC = """
def power(a: any) -> any { return a ** 2; }
def power_of(a: any, b: any) -> any { return a ** b; }
def neg_power(a: any, b: any) -> any { return (-a) ** b; }
def floor_div(a: any, b: any) -> any { return a // b; }
def floor_div_in_place(a: any, b: any) -> any { a //= b; return a; }
def int_floor_div_in_place(a: int, b: int) -> int { a //= b; return a; }
""";

test "power and floor division on untyped operands keep their operator" {
    js = compile_client(UNTYPED_OPS_SRC);
    assert "return (a ** 2);" in js , js;
    assert "(a + 2)" not in js , js;
    assert "return ((-a) ** b);" in js , js;
    assert "a = Math.floor((a / b));" in js , js;
    if not shutil.which("node") {
        testskip("node not on PATH");
    }
    probe = """
console.log(JSON.stringify([
    power(3), power_of(2, 10), neg_power(2, 3),
    floor_div(7, 2), floor_div(-7, 2),
    floor_div_in_place(9, 2), int_floor_div_in_place(-9, 2)
]));
""";
    assert run_probe(js, probe) == [9, 1024, -8, 3, -4, 4, -5] , js;
}

glob AWAITED_POWER_SRC = """
async def num() -> int { return 3; }
async def ratio() -> float { return 2.0; }
async def int_base(n: int) -> any { return (await num()) ** n; }
async def float_base(n: float) -> any { return (await ratio()) ** n; }
async def awaited_exponent(n: int) -> any { return n ** (await num()); }
def negated_base(b: int, n: int) -> any { return (-b) ** n; }
""";

test "an awaited or negated base of a power stays parenthesized" {
    js = compile_client(AWAITED_POWER_SRC);
    assert "((await num()) ** n)" in js , js;
    assert "((await ratio()) ** n)" in js , js;
    assert "await num() **" not in js , js;
    if not shutil.which("node") {
        testskip("node not on PATH");
    }
    probe = """
console.log(JSON.stringify([
    await int_base(2), await float_base(3.0), await awaited_exponent(2),
    negated_base(2, 3)
]));
""";
    assert run_probe(js, probe) == [9, 8, 8, -8] , js;
}

glob UNRESOLVED_KWARGS_SRC = """
glob made: list[int] = [];
def opts() -> dict[str, int] { made.append(1); return {"a": 1}; }
def more() -> dict[str, int] { return {"b": 2}; }
def spread_kw(x: any, kw: dict[str, int]) -> any { return x.f(1, **kw); }
def named_kw(x: any) -> any { return x.f(1, 2, b=3); }
def star_and_kw(x: any, xs: list[int]) -> any { return x.f(*xs, c=1); }
def two_spreads(x: any) -> any { return x.f(1, **opts(), **more()); }
def only_kw(x: any) -> any { return x.f(c=1); }
""";

test "a call to an unresolved target keeps its positional arguments beside keywords" {
    js = compile_client(UNRESOLVED_KWARGS_SRC);
    assert "x.f(1, {...kw})" in js , js;
    assert "x.f(1, 2, {b: 3})" in js , js;
    if not shutil.which("node") {
        testskip("node not on PATH");
    }
    probe = """
const rec = {f: (...args) => args};
console.log(JSON.stringify([
    spread_kw(rec, {b: 2}), named_kw(rec), star_and_kw(rec, [4, 5]),
    two_spreads(rec), made.length, only_kw(rec)
]));
""";
    assert run_probe(js, probe)
        == [
            [1, {"b": 2}],
            [1, 2, {"b": 3}],
            [4, 5, {"c": 1}],
            [1, {"a": 1, "b": 2}],
            1,
            [{"c": 1}]
        ] , js;
}
