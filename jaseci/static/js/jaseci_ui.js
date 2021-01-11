foc_state = {
    graph: null,
    sentinel: null,
    walker: null,
    node: null,
    edge: null,
    highlighted: null
};

function output(text) {
    output_view.replaceRange(text + "\n", { line: Infinity });
}

function reset_foc_state() {
    // see render graph for graph clearing
    foc_state.sentinel = null;
    foc_state.walker = null;
    foc_state.highlighted = null;
    code.setValue("");
    code.setOption("readOnly", "nocursor");
    json_view.setValue("");
}

function reset_graph() {
    foc_state.graph = null;
    clearAll();
    reset_foc_state();
}

function clear_highlight() {
    if (foc_state.highlighted) {
        document.getElementById(foc_state.highlighted.toString()).style[
            "background-color"
        ] = "";
    }
}

function highlight(i) {
    foc_state.highlighted = i;
    document.getElementById(i.toString()).style["background-color"] = "#ddffdd";
    show_json(i);
}

function show_json(i) {
    if (!i) {
        json_view.setValue("");
        return;
    }
    $.get("?op=obj_to_json&id=" + i.toString(), function (data, status) {
        json_view.setValue(data);
    });
}

function show_code() {
    $.get("?op=get_sentinel_code&id=" + foc_state.sentinel.toString(), function (
        data,
        status
    ) {
        code.setValue(data);
    });
    code.setOption("readOnly", false);
}

function render_graph() {
    $.get("?op=render_vis_graph&id=" + foc_state.graph.toString(), function (
        data,
        status
    ) {
        clearAll();
        eval(data);
    });
}

function check_update_graph(id) {
    graph = document.getElementById(id.toString()).getAttribute("graph");
    if (graph == foc_state.graph) {
        return;
    }
    foc_state.graph = graph;
    render_graph();
}

function select_graph(g) {
    clear_highlight();
    reset_foc_state();
    foc_state.graph = g;
    highlight(foc_state.graph);
    render_graph();
}

function select_sentinel(s) {
    clear_highlight();
    reset_foc_state();
    foc_state.sentinel = s;
    highlight(foc_state.sentinel);
    check_update_graph(s);
    show_code();
}

function select_walker(w) {
    clear_highlight();
    reset_foc_state();
    foc_state.walker = w;
    highlight(foc_state.walker);
    sent = document.getElementById(w.toString()).getAttribute("sentinel");
    foc_state.sentinel = sent;
    check_update_graph(foc_state.walker);
    //show_code();
}

function select_node(n) {
    foc_state.node = n;
    show_json(n);
}

function select_edge(e) {
    foc_state.edge = e;
}

function update_console() {
    $.get("?op=get_console", function (data, status) {
        if (output_view.getValue() != data) {
            output_view.setValue(data);
            output_view.setCursor(output_view.lastLine());
        }
    });
}

function save_code() {
    text = encodeURIComponent(code.getValue());
    sid = foc_state.sentinel.toString();
    $.get("?op=code_update&id=" + sid + "&text=" + text + "", function () { });
    // Stop normal link behavior
    return false;
}

$(".main-panel-left").resizable({
    handleSelector: ".main-splitter",
    resizeHeight: false
});
$(".bottom-panel-left").resizable({
    handleSelector: ".bottom-splitter",
    resizeHeight: false
});

// function addItem(){
// 	var ul = document.getElementById("dynamic-list");
//   var candidate = document.getElementById("candidate");
//   var li = document.createElement("li");
//   li.setAttribute('id',candidate.value);
//   li.appendChild(document.createTextNode(candidate.value));
//   ul.appendChild(li);
// }

// function removeItem(){
// 	var ul = document.getElementById("dynamic-list");
//   var candidate = document.getElementById("candidate");
//   var item = document.getElementById(candidate.value);
//   ul.removeChild(item);
// }

$(document).ready(function () {
    code = CodeMirror.fromTextArea(code_text, { lineNumbers: true });
    json_view = CodeMirror.fromTextArea(info1, {
        lineNumbers: true,
        lineWrapping: true
    });
    // stats = CodeMirror.fromTextArea(info2, {
    //     lineNumbers: false,
    //     lineWrapping: true
    // });
    output_view = CodeMirror.fromTextArea(info3, {
        lineNumbers: true,
        lineWrapping: true
    });
    code.setOption("readOnly", "nocursor");
    json_view.setOption("readOnly", true);
    // stats.setOption("readOnly", "nocursor");
    output_view.setOption("readOnly", "nocursor");
    // Set trigger and container variables
    (assets_view = $(".assets_view")),
        (code_view = $(".code_view")),
        (graph_view = $(".graph_view"));

    // On selection
    assets_view.on("click", ".select_graph", function () {
        select_graph(this.id);
    });
    assets_view.on("click", ".select_sentinel", function () {
        select_sentinel(this.id);
    });
    assets_view.on("click", ".select_walker", function () {
        select_walker(this.id);
    });
    assets_view.on("click", ".select_node", function () {
        select_node(this.id);
    });
    assets_view.on("click", ".select_edge", function () {
        select_edge(this.id);
    });

    assets_view.on("click", "#new_graph", function () {
        $.get("?op=create_graph", function (data, status) {
            $("#assets").html(data);
            update_console();
        });
    });

    assets_view.on("click", "#new_sentinel", function () {
        if (!foc_state.graph) {
            return;
        }
        $.get("?op=create_sentinel&id=" + foc_state.graph.toString(), function (
            data,
            status
        ) {
            $("#assets").html(data);
            highlight(foc_state.highlighted);
            update_console();
        });
    });

    assets_view.on("click", "#delete", function () {
        if (!foc_state.highlighted) {
            return;
        }
        if (!confirm("Are you sure you want to do this?")) {
            return;
        }
        $.get("?op=delete&id=" + foc_state.highlighted.toString(), function (
            data,
            status
        ) {
            $("#assets").html(data);
            reset_graph();
            update_console();
        });
    });

    code_view.on("keydown", $("code_text"), function () {
        if (typeof this.timehandle === "number") {
            clearTimeout(this.timehandle);
        }
        this.timehandle = setTimeout(function () {
            save_code();
        }, 1000);
    });

    code_view.on("click", "#register_code", function () {
        if (!foc_state.sentinel) {
            return;
        }
        $.get("?op=register_code&id=" + foc_state.sentinel.toString(), function (
            data,
            status
        ) {
            $("#assets").html(data);
            highlight(foc_state.highlighted);
            update_console();
            render_graph();
        });
    });

    graph_view.on("click", "#place_walker", function () {
        if (!foc_state.node) {
            console.log("WTF");
        }
        if (!foc_state.walker || !foc_state.node) {
            return;
        }
        $.get(
            "?op=prime_walker&id=" +
            foc_state.walker.toString() +
            "&node=" +
            foc_state.node,
            function (data, status) {
                highlight(foc_state.highlighted);
                update_console();
            }
        );
    });

    graph_view.on("click", "#step_walker", function () {
        if (!foc_state.walker) {
            return;
        }
        $.get("?op=step_walker&id=" + foc_state.walker.toString(), function (
            data,
            status
        ) {
            highlight(foc_state.highlighted);
            update_console();
            console.log(data)
            render_graph();
        });
    });

    graph_view.on("click", "#run_walker", function () {
        if (!foc_state.walker) {
            return;
        }
        var consoleRefresher = setInterval(update_console, 100);
        $.get("?op=run_walker&id=" + foc_state.walker.toString(), function (
            data,
            status
        ) {
            highlight(foc_state.highlighted);
            clearInterval(consoleRefresher);
            update_console();
            console.log(data)
            render_graph();
        });
    });

    network.on("click", function (params) {
        if (params.nodes.length != 0) {
            select_node(params.nodes[0]);
        } else {
            select_node(null);
        }
        if (params.edges.length != 0) {
            select_edge(params.edges[0]);
        } else {
            select_edge(null);
        }
    });
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != "") {
                var cookies = document.cookie.split(";");
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == name + "=") {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});
