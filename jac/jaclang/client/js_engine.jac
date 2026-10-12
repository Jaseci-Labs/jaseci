def engine_dir -> str {
    import from jaclang.artifacts.router { require }
    found = require("js-engine").found;
    assert found is not None;
    return found.path;
}

def node_executable -> str {
    import from jaclang.client.js_runtime { ensure_node_link }
    return ensure_node_link(engine_dir());
}
