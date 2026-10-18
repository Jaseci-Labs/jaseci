import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from jaclang.client.vite_client_bundle { ViteClientBundleBuilder }
import from jaclang.client.client_bundle { ClientBundleError }
import from jaclang.project.config { set_config }

def _compiler(project: Path) -> any {
    (project / "package.json").write_text('{"name":"imports","version":"0.0.0"}');
    (project / "jac.toml").write_text(
        '[project]\nname = "imports"\nkind = "web-app"\n'
        '[placement.pins]\n"provider" = "client"\n'
    );
    builder = ViteClientBundleBuilder(vite_package_json=project / "package.json");
    compiler = builder._get_compiler().jac_client_compiler;
    compiler.compiled_dir = project / "compiled";
    return compiler;
}

test "annotation imports disappear but values and module effects survive" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "provider.jac").write_text(
            'obj Session { has name: str = ""; }\n'
            'obj:pub Value { has name: str = "value"; }\n'
            'def:pub session -> Session { return Session(); }\n'
        );
        (project / "main.jac").write_text(
            'import from .provider { Session as State, Value as Item, session }\n'
            'def:pub app -> any {\n'
            '    state: State = session();\n'
            '    item = Item();\n'
            '    return <div>{state.name}{item.name}</div>;\n'
            '}\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "main.js").read_text();
            imports = "\n".join(
                line
                for line in js.splitlines()
                if line.startswith("import ")
            );
            assert "Session" not in imports , imports;
            assert "Value as Item" in imports , imports;
            assert "session" in imports , imports;
            # The same checks must apply when compiler artifacts come from cache.
            compiler.emit_dependencies(project / "main.jac", source_root=project);
        } finally {
            set_config(None);
        }
    }
}

def _export_lines(js: str) -> list[str] {
    return [
        line
        for line in js.splitlines()
        if line.startswith("export {")
    ];
}

test "a client-pinned module exports the plain names client importers use" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "provider.jac").write_text(
            'obj Hidden { has name: str = ""; }\n'
            'glob LABELS: dict[str, str] = {"new": "New"};\n'
        );
        (project / "main.jac").write_text(
            'import from .provider { Hidden, LABELS }\n'
            'def:pub app -> any {\n'
            '    value = Hidden();\n'
            '    return <div>{value.name}{LABELS["new"]}</div>;\n'
            '}\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "provider.js").read_text();
            assert _export_lines(js) == ["export {Hidden, LABELS};"] , js;
        } finally {
            set_config(None);
        }
    }
}

test "a name is exported to its client importers however its module placed it" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "shared.jac").write_text(
            'glob CATEGORY_LIST: list[str] = ["Electronics", "Fashion"];\n'
            'glob CONDITION_LABELS: dict[str, str] = {"new": "New"};\n'
            'def shout(text: str) -> str { return text.upper(); }\n'
            'def Card(title: str) -> JsxElement { return <b>{title}</b>; }\n'
            'def Local(title: str) -> JsxElement { return <i>{title}</i>; }\n'
            'def:pub Badge(value: str) -> JsxElement {\n'
            '    return <span>{CONDITION_LABELS[value]}<Local title={shout(value)} /></span>;\n'
            '}\n'
        );
        (project / "main.jac").write_text(
            'import from .shared { Badge, Card, CATEGORY_LIST, CONDITION_LABELS, shout }\n'
            'def:pub app -> any {\n'
            '    return <div>\n'
            '        <Badge value="new" />\n'
            '        <Card title={shout(CATEGORY_LIST[0])} />\n'
            '        {CONDITION_LABELS["new"]}\n'
            '    </div>;\n'
            '}\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "shared.js").read_text();
            assert _export_lines(js)
                == [
                    "export {Badge, CATEGORY_LIST, CONDITION_LABELS, Card, shout};"
                ] , js;
        } finally {
            set_config(None);
        }
    }
}

test "names no client module imports stay unexported, keeping refresh boundaries" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "widgets.jac").write_text(
            'def label(text: str) -> str { return text.upper(); }\n'
            'def:pub Card(title: str) -> JsxElement { return <b>{label(title)}</b>; }\n'
        );
        (project / "main.jac").write_text(
            'import from .widgets { Card }\n'
            'def:pub app -> any { return <Card title="x" />; }\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "widgets.js").read_text();
            assert _export_lines(js) == ["export {Card};"] , js;
            assert "/*jac:refresh-boundary*/" in js , js;
        } finally {
            set_config(None);
        }
    }
}

test "the held pull set records names other client modules import" {
    import os;
    import jaclang.compiler.frontend.unitree as uni;
    import from jaclang.compiler.driver.program { JacProgram }
    import from jaclang.compiler.driver.unit_products { client_pulled_indexes }
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        _compiler(project);
        (project / "shared.jac").write_text(
            'glob LABELS: dict[str, str] = {"new": "New"};\n'
            'def Card(title: str) -> JsxElement { return <b>{title}{LABELS["new"]}</b>; }\n'
            'def Local(title: str) -> JsxElement { return <i>{title}</i>; }\n'
        );
        (project / "main.jac").write_text(
            'import from .shared { Card, LABELS }\n'
            'def:pub app -> any { return <div><Card title="x" />{LABELS["new"]}</div>; }\n'
        );
        try {
            prog = JacProgram();
            prog.compile(str(project / "main.jac"), no_cgen=False);
            shared = [
                m
                for (path, m) in prog.mod.hub.items()
                if os.path.basename(path) == "shared.jac"
            ];
            assert shared , list(prog.mod.hub.keys());
            body = shared[0].body;
            assert all(
                isinstance(stmt, uni.ContextAwareNode) and not stmt.codespace_dual
                for stmt in body
            );
            assert client_pulled_indexes(shared[0]) == [0, 1] , [
                stmt?.client_imported for stmt in body
            ];
        } finally {
            set_config(None);
        }
    }
}

test "the client graph rejects a runtime import its provider does not export" {
    import from jaclang.compiler.driver.client_graph { collect_client_graph }
    import from jaclang.compiler.frontend.codeinfo { ClientArtifact, ClientManifest }
    with TemporaryDirectory() as tmp {
        project = Path(tmp).resolve();
        main = project / "main.jac";
        provider = project / "provider.jac";
        main.write_text("");
        provider.write_text("");
        artifacts = {
            main: ClientArtifact(
                js="",
                manifest=ClientManifest(runtime_imports={str(provider): ["Hidden"]})
            ),
            provider: ClientArtifact(js="", manifest=ClientManifest())
        };
        def artifact_of(path: Path) -> ClientArtifact {
            return artifacts[path];
        }
        def variant_of(path: Path) -> Path {
            return path;
        }
        failed = False;
        try {
            collect_client_graph([main], artifact_of, variant_of, set(), set());
        } except ClientBundleError as error {
            failed = True;
            assert "runtime import(s) Hidden" in str(error) , str(error);
            assert "provider.jac" in str(error) , str(error);
        }
        assert failed , "a runtime import with no matching export reached the bundler";
    }
}

test "an annotation-only binding preserves module evaluation" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "provider.jac").write_text(
            'obj Session { has name: str = ""; }\n'
            'glob:pub loads: int = 0;\n'
            'with entry { loads += 1; }\n'
        );
        (project / "main.jac").write_text(
            'import from .provider { Session }\n'
            'def:pub app(value: Session) -> any { return <div>{value.name}</div>; }\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "main.js").read_text();
            assert 'import "./provider.js";' in js , js;
            assert (project / "compiled" / "provider.js").is_file();
        } finally {
            set_config(None);
        }
    }
}

test "client artifact caches preserve the runtime import contract" {
    import pickle;
    import from jaclang.compiler.frontend.codeinfo { ClientArtifact, ClientManifest }
    import from jaclang.compiler.driver.compiler {
        client_artifact_bytes,
        client_artifact_from_bytes
    }
    manifest = ClientManifest(runtime_imports={"provider.jac": ["Value"]});
    artifact = ClientArtifact(js="", manifest=manifest);
    restored = client_artifact_from_bytes(client_artifact_bytes(artifact));
    assert restored is not None;
    assert restored.manifest.runtime_imports == manifest.runtime_imports;
    legacy = pickle.dumps(("", manifest, [], [], {}, ""));
    assert client_artifact_from_bytes(legacy) is None;
}

test "jsx references and shadowed names retain their runtime imports" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        (project / "provider.jac").write_text(
            'def:pub Button -> any { return <button>ok</button>; }\n'
            'def:pub value -> int { return 1; }\n'
        );
        (project / "main.jac").write_text(
            'import from .provider { Button, value }\n'
            'def shadow(value: int) -> int { return value; }\n'
            'def:pub app -> any { assert value() == 1; return <Button />; }\n'
        );
        try {
            compiler.emit_dependencies(project / "main.jac", source_root=project);
            js = (project / "compiled" / "main.js").read_text();
            imports = "\n".join(
                line
                for line in js.splitlines()
                if line.startswith("import ")
            );
            assert "Button" in imports and "value" in imports , imports;
        } finally {
            set_config(None);
        }
    }
}

test "native runtime emits dependencies for bare imports" {
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        try {
            (js, exports) = compiler.compile_runtime_utils(
                compiler.NATIVE_RUNTIME_FILE
            );
            for name in ["useJacState", "jacSetToken"] {
                assert name in exports , f"Native runtime is missing {name}";
                assert f"function {name}(" in js , f"Missing implementation: {name}";
            }
            assert "html_tag_map.js" in js;
            assert (
                project / "compiled" / "targets" / "react_native" / "html_tag_map.js"
            ).is_file();
        } finally {
            set_config(None);
        }
    }
}
