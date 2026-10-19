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

test "missing runtime exports fail before either client bundler starts" {
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
        assert failed , "invalid runtime imports reached the bundler";
    }
}

test "client providers export exactly the names client importers bind" {
    # (provider, provider source, importer source, export line, refresh boundary,
    #  held pull indexes)
    cases = [
        (
            "shared",
            'glob CATEGORY_LIST: list[str] = ["Electronics", "Fashion"];\n'
            'glob CONDITION_LABELS: dict[str, str] = {"new": "New"};\n'
            'def shout(text: str) -> str { return text.upper(); }\n'
            'def Card(title: str) -> JsxElement { return <b>{title}</b>; }\n'
            'def Local(title: str) -> JsxElement { return <i>{title}</i>; }\n'
            'def:pub Badge(value: str) -> JsxElement {\n'
            '    return <span>{CONDITION_LABELS[value]}<Local title={shout(value)} /></span>;\n'
            '}\n',
            'import from .shared { Badge, Card, CATEGORY_LIST, CONDITION_LABELS, shout }\n'
            'def:pub app -> any {\n'
            '    return <div>\n'
            '        <Badge value="new" />\n'
            '        <Card title={shout(CATEGORY_LIST[0])} />\n'
            '        {CONDITION_LABELS["new"]}\n'
            '    </div>;\n'
            '}\n',
            "export {Badge, CATEGORY_LIST, CONDITION_LABELS, Card, shout};",
            False,
            [0, 1, 2, 3, 5]
        ),
        (
            "provider",
            'obj Hidden { has name: str = ""; }\n'
            'glob LABELS: dict[str, str] = {"new": "New"};\n',
            'import from .provider { Hidden, LABELS }\n'
            'def:pub app -> any {\n'
            '    value = Hidden();\n'
            '    return <div>{value.name}{LABELS["new"]}</div>;\n'
            '}\n',
            "export {Hidden, LABELS};",
            False,
            [0, 1]
        ),
        (
            "widgets",
            'def label(text: str) -> str { return text.upper(); }\n'
            'def:pub Card(title: str) -> JsxElement { return <b>{label(title)}</b>; }\n',
            'import from .widgets { Card }\n'
            'def:pub app -> any { return <Card title="x" />; }\n',
            "export {Card};",
            True,
            [1]
        ),

    ];
    with TemporaryDirectory() as tmp {
        set_config(None);
        project = Path(tmp);
        compiler = _compiler(project);
        try {
            for (name, source, importer, export_line, boundary, pulled) in cases {
                (project / f"{name}.jac").write_text(source);
                (project / f"use_{name}.jac").write_text(importer);
                compiler.emit_dependencies(
                    project / f"use_{name}.jac", source_root=project
                );
                js = (project / "compiled" / f"{name}.js").read_text();
                exports = [
                    line
                    for line in js.splitlines()
                    if line.startswith("export {")
                ];
                assert exports == [export_line] , (name, js);
                assert ("/*jac:refresh-boundary*/" in js) == boundary , (name, js);
                artifact = compiler.jac_compiler.compile_module(
                    project / f"{name}.jac"
                );
                assert artifact.pulled == pulled , (name, artifact.pulled);
            }
        } finally {
            set_config(None);
        }
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
