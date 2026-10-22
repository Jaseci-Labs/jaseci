test "code blocks are the jac fences, in order" {
    md = "intro\n\n```jac\nwith entry { print(1); }\n```\n\n```bash\njac run x.jac\n```\n\n```jac\nnode A {}\n```\n";
    assert code_blocks(md) == ["with entry { print(1); }", "node A {}"];
}

test "runnable programs run and server or llm code is only checked" {
    assert block_mode("with entry { print(1); }") == "run";
    assert block_mode("node A {}") == "check";
    assert block_mode("walker:pub w { can go with Root entry {} }\nwith entry {}")
        == "check";
    assert block_mode("def f -> str by llm();\nwith entry { print(f()); }") == "check";
}

test "a correct program passes and a broken one reports why" {
    good = verify_block(
        0,
        "node Item {\n    has label: str = \"one\";\n}\n\nwith entry {\n    print(Item().label);\n}"
    );
    assert good.ok , good.detail;
    assert good.mode == "run";
    bad = verify_block(1, "with entry {\n    print(undefined_name_here);\n}");
    assert not bad.ok;
    assert bad.detail != "";
}
