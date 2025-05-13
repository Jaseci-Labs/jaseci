import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from pathlib import Path
import json
import ast

IGNORE_DIR = {"__pycache__", ".git", "node_modules", ".DS_Store", "thumbs.db", "env"}
INCLUDE_EXTENSION = {'.py'}
base_path = (Path(__file__).parent.parent).resolve()

def extract_py_info(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=str(file_path))
    
    def get_doc(obj):
        return ast.get_docstring(obj) or ""
    return {
        "module_docstring": get_doc(node),
        "imports": [n.names[0].name for n in node.body if isinstance(n, ast.Import)],
        "functions": [
            {
                "name": func.name,
                "docstring": get_doc(func)
            }
            for func in node.body if isinstance(func, ast.FunctionDef)
        ]
    }


def dir_to_dict(path: Path):
    tree = {}
    for item in path.iterdir():
        if item.name in IGNORE_DIR:
            continue
        if item.is_dir():
            tree[item.name] = dir_to_dict(item)
        elif item.suffix in INCLUDE_EXTENSION:
            tree[item.name] = extract_py_info(item)
    return tree

tree = {base_path.name: dir_to_dict(base_path)}


G = nx.DiGraph()

def add_nodes(parent, subtree):
    for name, val in subtree.items():
        node_id = parent + "/" + name if parent else name
        if isinstance(val, dict) and "imports" in val:
            G.add_node(node_id, is_file=True, imports=val["imports"],
                       functions=[fn["name"] for fn in val["functions"]],
                       doc=val["module_docstring"])
        else:
            G.add_node(node_id, is_file=False)
            add_nodes(node_id, val)
        if parent:
            G.add_edge(parent, node_id)

add_nodes("", tree)
pos = graphviz_layout(G, prog="dot")

edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="#888"), hoverinfo="none")

node_x, node_y, text, customdata, node_colors = [], [], [], [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    text.append(Path(node).name)
    data = G.nodes[node]
    is_file = data["is_file"]
    has_content = is_file and (data.get("imports") or data.get("functions") or data.get("doc"))

    customdata.append({
        "id": node,
        "is_file": is_file,
        "imports": data.get("imports", []),
        "functions": data.get("functions", []),
        "doc": data.get("doc", "")
    })

    if not is_file:
        node_colors.append("#5DADE2") 
    elif has_content:
        node_colors.append("#28D7A2")  
    else:
        node_colors.append("#999999")  

node_trace = go.Scatter(
    x=node_x, y=node_y, mode="markers+text", text=text,
    textposition="bottom center", hoverinfo="text",
    marker=dict(size=18, color=node_colors),
    customdata=customdata
)

fig = go.Figure(data=[edge_trace, node_trace])

fig.update_layout(
    dragmode="pan",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    margin=dict(l=0, r=0, t=0, b=0),
    plot_bgcolor="white",
    showlegend=False
)

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id="file-graph",
        figure=fig,
        config={
            "scrollZoom": True,
            "displayModeBar": False,
            "displaylogo": False
        },
        style={"height": "100vh", "width": "100vw"}
    ),

    html.Div(id="code-modal-container", children=[
        html.Div(id="code-modal", children=[
            html.Button("✕", id="close-button", n_clicks=0, style={
                "position": "absolute", "top": "8px", "right": "12px",
                "background": "transparent", "border": "none",
                "fontSize": "20px", "color": "#d4d4d4", "cursor": "pointer"
            }),
            html.Div(id="code-display", style={
                "backgroundColor": "#1e1e1e",
                "color": "#D4D4D4",
                "fontFamily": "Consolas, monospace",
                "whiteSpace": "pre-wrap",
                "padding": "12px",
                "borderRadius": "8px",
                "fontSize": "14px",
                "maxHeight": "70vh",
                "overflowY": "auto"
            })
        ], style={
            "display": "none",
            "position": "fixed",
            "top": "0", "left": "0",
            "width": "100%", "height": "100%",
            "backgroundColor": "rgba(0,0,0,0.7)",
            "zIndex": "9999",
            "justifyContent": "center",
            "alignItems": "center",
            "padding": "40px",
            "boxSizing": "border-box"
        })
    ])
], style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0, "overflow": "hidden"})

@app.callback(
    Output("code-display", "children"),
    Input("file-graph", "clickData")
)

def display_code(clickData):
    if not clickData:
        return ""

    point = clickData["points"][0]["customdata"]
    if not point["is_file"] or (
        not point["imports"] and not point["functions"] and not point["doc"]
    ):
        return f"# {Path(point['id']).name} is empty or not a file."

    lines = []

    for imp in point["imports"]:
        lines.append(html.Span([
            html.Span("import ", style={"color": "#569CD6"}),
            html.Span(imp, style={"color": "#9CDCFE"})
        ]))
        lines.append(html.Br())
    lines.append(html.Br())

    if point["doc"]:
        lines.append(html.Span(f'""" {point["doc"]} """', style={"color": "#6A9955", "fontStyle": "italic"}))
        lines.append(html.Br())
        lines.append(html.Br())

    for fn in point["functions"]:
        lines.append(html.Span([
            html.Span("def ", style={"color": "#4EC9B0"}),
            html.Span(fn, style={"color": "#DCDCAA"}),
            html.Span("():", style={"color": "#D4D4D4"})
        ]))
        lines.append(html.Br())
        lines.append(html.Span("    pass", style={"color": "#D4D4D4"}))
        lines.append(html.Br())
        lines.append(html.Br())

    return lines

@app.callback(
    Output("code-modal", "style"),
    Input("file-graph", "clickData"),
    Input("close-button", "n_clicks"),
    State("code-modal", "style")
)

def toggle_modal(clickData, close_clicks, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger == "close-button":
        return {**current_style, "display": "none"}

    if trigger == "file-graph" and clickData:
        point = clickData["points"][0]["customdata"]
        if point["is_file"] and (
            point["imports"] or point["functions"] or point["doc"]
        ):
            return {**current_style, "display": "flex"}

    return current_style

if __name__ == "__main__":
    app.run(debug=True)
