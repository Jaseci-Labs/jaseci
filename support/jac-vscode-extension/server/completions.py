from typing import Optional
from pygls.server import LanguageServer
import inspect
from jaseci.actions.standard import file, std, date, mail, net, vector


from lsprotocol.types import (
    CompletionParams,
    CompletionList,
    CompletionItem,
    CompletionItemKind,
)


std_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(std, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]
file_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(file, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]
date_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(date, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]
vector_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(vector, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]

mail_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(mail, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]

net_actions = [
    {
        "name": func[0],
        "args": inspect.getfullargspec(func[1]).args,
        "doc": inspect.getdoc(func[1]),
    }
    for func in inspect.getmembers(net, inspect.isfunction)
    if "@jaseci_action" in inspect.getsource(func[1])
]

action_modules = {
    "std": std_actions,
    "file": file_actions,
    "date": date_actions,
    "vector": vector_actions,
    "mail": mail_actions,
    "net": net_actions,
}


def get_builtin_action(action_name: str, module_name: str) -> str:
    """Returns the docstring for an action"""
    for action in action_modules[module_name]:
        if action["name"] == action_name:
            return action
    return None


def completions(
    server: LanguageServer, params: Optional[CompletionParams] = None
) -> CompletionList:
    """Returns completion items."""
    # get characters before the cursor
    doc = server.workspace.get_document(params.text_document.uri)
    line = doc.source.splitlines()[params.position.line]
    before_cursor = line[: params.position.character]

    # get the last word before the cursor
    last_word = before_cursor.split()[-1]

    # if we are in a string, don't return any completions
    if '("' in last_word or '")' in last_word:
        return CompletionList(is_incomplete=False, items=[])

    # completion for jaseci built in actions
    for mod in action_modules.keys():
        if (
            last_word.find(mod + ".") != -1
            and last_word.find(".", last_word.find(mod + ".") + len(mod + ".")) == -1
            and last_word.find("(", last_word.find(mod + ".") + len(mod + ".")) == -1
        ):
            return CompletionList(
                is_incomplete=False,
                items=[
                    CompletionItem(
                        label=action["name"], kind=CompletionItemKind.Function
                    )
                    for action in action_modules[mod]
                ],
            )

    # handle completion for architypes references
    if "node::" in last_word and hasattr(doc, "architypes"):
        node_names = [node["name"] for node in doc.architypes["nodes"]]

        for dep in doc.dependencies.values():
            architypes = dep["architypes"]
            node_names.extend([node["name"] for node in architypes["nodes"]])

        return CompletionList(
            is_incomplete=False,
            items=[
                CompletionItem(label=node_name, kind=CompletionItemKind.Class)
                for node_name in node_names
            ],
        )

    if "walker::" in last_word and hasattr(doc, "architypes"):
        walker_names = [walker["name"] for walker in doc.architypes["walkers"]]
        for dep in doc.dependencies.values():
            architypes = dep["architypes"]
            walker_names.extend([node["name"] for node in architypes["walkers"]])
        return CompletionList(
            is_incomplete=False,
            items=[
                CompletionItem(label=node_name, kind=CompletionItemKind.Function)
                for node_name in walker_names
            ],
        )

    # handle completion for edges
    for item in ["+[", "<+[", "-[", "<-[", "(-[", "(<-["]:
        if last_word.startswith(item) or last_word.startswith("!" + item):
            edge_names = [edge["name"] for edge in doc.architypes["edges"]]
            for dep in doc.dependencies.values():
                architypes = dep["architypes"]
                edge_names.extend([node["name"] for node in architypes["edges"]])

            return CompletionList(
                is_incomplete=False,
                items=[
                    CompletionItem(label=edge_name, kind=CompletionItemKind.Interface)
                    for edge_name in edge_names
                ],
            )

    return CompletionList(
        is_incomplete=False,
        items=[],
    )
