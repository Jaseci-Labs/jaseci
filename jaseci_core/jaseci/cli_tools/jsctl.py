"""
Command line tool for Jaseci
"""

import functools
import json
import os
import pickle
import webbrowser
import click
import requests
from click_shell import shell
from click.testing import CliRunner
from jaseci import __version__
from jaseci.prim.super_master import SuperMaster
from jaseci.utils.utils import copy_func
from .book_tools import Book, modifiedBook
from jaseci.utils.file_handler import FileHandler
from jaseci.utils.utils import logger, perf_test_start, perf_test_stop, find_first_api
from jaseci.jsorc.jsorc import JsOrc
from prettytable import PrettyTable

session = None


def reset_state():
    global session
    session = {
        "filename": "js.session",
        "user": [JsOrc.super_master(name="admin")],
        "mem-only": session["mem-only"] if session is not None else False,
        "connection": {"url": None, "token": None, "headers": None},
    }
    session["master"] = session["user"][0]


reset_state()


def is_connected():
    return bool(session["connection"]["url"])


def get_prompt():
    if is_connected():
        return "@jaseci > "
    else:
        return "jaseci > "


def get_intro():
    return f"Jaseci {__version__}\n" + "Starting Shell..."


@shell(prompt=get_prompt, intro=get_intro())
@click.option(
    "--filename", "-f", default="js.session", help="Specify filename for session state."
)
@click.option(
    "--mem-only", "-m", is_flag=True, help="Set true to not save file for session."
)
def jsctl(filename, mem_only):
    """
    The Jaseci Command Line Interface
    """
    global session
    if not mem_only and os.path.isfile(filename):
        with open(filename, "rb") as f:
            session = pickle.load(f)
    session["mem-only"] = mem_only
    session["filename"] = filename if not mem_only else None


@click.group()
def jac():
    """
    Jac tool for building, running, and disassembling Jac programs
    """
    global session
    session["mem-only"] = True


def remote_api_call(payload, api_name):
    """
    Constructs and issues call to remote server
    NOTE: Untested
    """
    path, api = find_first_api(
        api_name,
        js_public=SuperMaster._public_api,
        js=SuperMaster._private_api,
        js_admin=SuperMaster._admin_api,
    )

    method = requests.post
    if api["allowed_methods"] != None and "post" not in api["allowed_methods"]:
        method = requests.get

    ret = method(
        session["connection"]["url"] + f"/{path}/{api_name}",
        json=payload,
        headers=session["connection"]["headers"],
    )
    if ret.status_code > 205:
        ret = f"Status Code Error {ret.status_code}\n{ret.json()}"
    elif ret.headers.get("Content-Type", None) == "application/octet-stream":
        file_handler = FileHandler.fromRequest(
            ret.content, ret.headers.get("Content-Disposition")
        )
        session["master"]._h.add_file_handler(file_handler)
        ret = file_handler.attr()
    else:
        ret = ret.json()
    return ret


def resolve_none_type(kwargs):
    for i in kwargs.keys():
        if kwargs[i] == "None":
            kwargs[i] = None


def has_profile(output):
    if isinstance(output, dict):
        if "profile" in output.keys():
            if "jac" in output["profile"].keys() and "perf" in output["profile"].keys():
                return True
    return False


def gen_pretty_table(csv_str):
    rows = csv_str.split("\n")
    row_width = len(rows[0].split(","))
    first_row = rows[0].split(",")
    if first_row[2] == "percall":
        first_row[2] = "percall_tot"
    try:
        table = PrettyTable(first_row)
        for i in rows[1:]:
            row = i.split(",")
            if len(row) != row_width:
                continue
            table.add_row(row)
        return table
    except Exception as e:
        click.echo(f"Something went wrong pretty printing profile: {e}")


def pretty_profile(output):
    click.echo("Jac Code Profile:")
    click.echo(gen_pretty_table(output["profile"]["jac"]))
    click.echo("\nInternal Jaseci Profile:")
    click.echo(gen_pretty_table(output["profile"]["perf"]))


def interface_api(api_name, is_public, is_cli_only, **kwargs):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    if "code" in kwargs and kwargs["code"]:
        if os.path.isfile(kwargs["code"]):
            with open(kwargs["code"], "r") as file:
                if (
                    api_name == "sentinel_register"
                    and "name" in kwargs
                    and kwargs["name"] == "default"
                ):
                    kwargs["name"] = kwargs["code"]
                kwargs["code"] = file.read()
        else:
            click.echo(f"Code file {kwargs['code']} not found!")
            return
    resolve_none_type(kwargs)
    if not is_cli_only and is_connected():
        out = remote_api_call(kwargs, api_name)
    elif is_public:
        out = session["master"].public_interface_to_api(kwargs, api_name)
    else:
        out = session["master"].general_interface_to_api(kwargs, api_name)
    d_out = out
    if isinstance(out, dict):
        if "report_custom" in out.keys() and out["report_custom"] is not None:
            out = out["report_custom"]
        elif "report_file" in out.keys() and out["report_file"] is not None:
            out = session["master"]._h.get_file_handler(out["report_file"]).attr()

    if isinstance(out, dict) or isinstance(out, list):
        out = json.dumps(out, indent=2)
    click.echo(out)
    if "output" in kwargs and kwargs["output"]:
        with open(kwargs["output"], "w") as f:
            f.write(out)
        click.echo(f'[saved to {kwargs["output"]}]')
    if not session["mem-only"]:
        with open(session["filename"], "wb") as f:
            pickle.dump(session, f)
    if has_profile(d_out):
        pretty_profile(d_out)


def extract_api_tree():
    """
    Generates a tree of command group names and function
    signatures in leaves from API function names in Master
    """
    api_funcs = {}
    for i in session["master"].all_apis() + session["master"]._cli_api:
        # Build hierarchy of command groups
        api_root = api_funcs
        for j in i["groups"]:
            if j not in api_root.keys():
                api_root[j] = {}
            api_root = api_root[j]
        api_root["leaf"] = [
            "_".join(i["groups"]),
            i["sig"],
            i in session["master"]._public_api,
            i["doc"],
            i["cli_args"],
            i in session["master"]._cli_api,
        ]
    return api_funcs


def build_cmd(group_func, func_name, leaf):
    """
    Generates Click function with options for each command
    group and leaf signatures
    leaf is format: [api_name, func_sig, is_public, func_doc]
    """

    f = functools.partial(
        copy_func(interface_api, func_name),
        api_name=leaf[0],
        is_public=leaf[2],
        is_cli_only=leaf[5],
    )
    f.__name__ = func_name
    f.__doc__ = leaf[3]

    func_sig = leaf[1]
    cli_args = leaf[4]
    for i in func_sig.parameters.keys():
        if i == "self":
            continue
        p_default = func_sig.parameters[i].default
        p_type = func_sig.parameters[i].annotation
        if p_type not in [int, bool, float]:
            p_type = str
        if i in cli_args:
            f = click.argument(f"{i}", type=p_type)(f)
        elif p_default is not func_sig.parameters[i].empty:
            f = click.option(
                f"-{i}",
                default=p_default if p_default is None else p_type(p_default),
                required=False,
                type=p_type,
            )(f)
        else:
            f = click.option(f"-{i}", required=True, type=p_type)(f)
    # to file option to dump response to a file
    f = click.option(
        "--output",
        "-o",
        default="",
        required=False,
        type=str,
        help="Filename to dump output of this command call.",
    )(f)
    return group_func.command()(f)


def cmd_tree_builder(location, group_func=jsctl, cmd_str=""):
    """
    Generates Click command groups from API tree recursively
    """
    for i in location.keys():
        loc = location[i]
        if "leaf" in loc:
            build_cmd(group_func, i, loc["leaf"])
            continue
        else:
            f = copy_func(lambda: None, i)
            f.__doc__ = f'Group of `{(cmd_str + " " + i).lstrip()}` commands'
            new_func = group_func.group()(f)
        cmd_tree_builder(loc, new_func, cmd_str + " " + i)


@click.command(help="Command to log into live Jaseci server")
@click.argument("url", type=str, required=True)
@click.option(
    "--username",
    "-u",
    required=True,
    prompt=True,
    help="Username to be used for login.",
)
@click.password_option(help="Password to be used for login.", confirmation_prompt=False)
def login(url, username, password):
    url = url[:-1] if url[-1] == "/" else url
    payload = {"email": username, "password": password}
    try:
        r = requests.post(url + "/user/token/", data=payload).json()
    except Exception:
        r = {"error": "Invalid url, username, or password."}
    if "token" in r.keys():
        session["connection"]["token"] = r["token"]
        session["connection"]["url"] = url
        session["connection"]["headers"] = {"Authorization": "token " + r["token"]}
        click.echo(f"Token: {r['token']}\nLogin successful!")
    else:
        click.echo("Login failed!\n")
    if not session["mem-only"]:
        with open(session["filename"], "wb") as f:
            pickle.dump(session, f)


@click.command(help="Launch Jaseci Studio")
def studio():
    token = session["connection"]["token"]

    if not token:
        click.echo(
            click.style(
                "It doesn't look like you're logged in to a Jaseci instance. Please log in to a Jaseci instance to use this command.\n",
                fg="red",
            )
        )
    else:
        url = session["connection"]["url"] + "/studio/"

        if token == "PUBLIC":
            click.echo(
                click.style(
                    "You are logged in as a public user. Please log in to a Jaseci instance to use this command.\n",
                    fg="red",
                )
            )

            webbrowser.open(url)
        else:
            click.echo(click.style("Launching Jaseci Studio...", fg="green"))
            click.echo(click.style("URL: ", fg="green", bold=True) + url)
            click.echo(click.style(f"Token: {token}", fg="green"))
            webbrowser.open(url + "?token=" + token)


@click.command(help="Command for unauthenticated log into live Jaseci server")
@click.argument("url", type=str, required=True)
def publogin(url):
    url = url[:-1] if url[-1] == "/" else url
    if requests.get(url).status_code <= 205:
        session["connection"]["token"] = "PUBLIC"
        session["connection"]["url"] = url
        session["connection"]["headers"] = {}
        click.echo("Login successful!")
    else:
        click.echo("Login failed!\n")
    if not session["mem-only"]:
        with open(session["filename"], "wb") as f:
            pickle.dump(session, f)


@click.command(help="Command to log out of live Jaseci server")
def logout():
    if session["connection"]["token"]:
        session["connection"]["token"] = None
        session["connection"]["url"] = None
        session["connection"]["headers"] = {}
        click.echo("Logout successful!")
    else:
        click.echo("You are not logged in!")


@click.command(help="Edit a file")
@click.argument("file", type=str, required=True)
def edit(file):
    click.edit(filename=file)


@click.command(help="List relevant files")
@click.option(
    "--all",
    "-a",
    is_flag=True,
    help="Flag for listing all files, not just relevant files",
)
def ls(all):
    for i in os.listdir():
        if all:
            click.echo(f"{i}")
        else:
            click.echo(f"{i}") if i.endswith(".jac") or i.endswith(".dot") else False


@click.command(help="Clear terminal")
def clear():
    click.clear()


@click.command(help="Reset jsctl (clears state)")
def reset():
    reset_state()
    click.echo("Jaseci State Cleared!")


@click.command(help="Run multiple commands sequentially from file")
@click.argument("filename", type=str, required=True)
@click.option("--profile", "-p", is_flag=True)
@click.option(
    "--output",
    "-o",
    default="",
    required=False,
    type=str,
    help="Filename to dump output of this command call.",
)
def script(filename, profile, output):
    if profile:
        prof = perf_test_start()
    if not os.path.isfile(filename):
        click.echo("File not found!")
        return
    with open(filename) as file:
        cmds = [line.rstrip() for line in file]
    if output:
        with open(output, "w") as f:
            f.write("Multi Command Script Output:\n")
    for i in cmds:
        res = CliRunner(mix_stderr=False).invoke(jsctl, i)
        click.echo(res.stdout)
        if output:
            with open(output, "a") as f:
                f.write(f"Output for {i}:\n")
                f.write(res.stdout)
    if profile:
        perf, graph = perf_test_stop(prof)
        click.echo(perf)
        click.echo(graph)
    if output:
        with open(output, "a") as f:
            if profile:
                f.write(f"\nProfile:\n")
                f.write(perf)
                f.write(graph)
        click.echo(f"[saved to {output}]")


@click.command(help="Internal book generation tools")
@click.argument("op", type=str, default="cheatsheet", required=True)
@click.option(
    "--output",
    "-o",
    default="",
    required=False,
    type=str,
    help="Filename to dump output of this command call.",
)
def booktool(op, output):
    out = ""
    if op == "cheatsheet":
        out = f"{Book().bookgen_api_cheatsheet(extract_api_tree())}"
    elif op == "stdlib":
        out = Book().bookgen_std_library()
    elif op == "mdcheatsheet":
        out = f"{modifiedBook().bookgen_api_cheatsheet(extract_api_tree())}"
    elif op == "mdstdlib":
        out = modifiedBook().bookgen_std_library()
    elif op == "classes":
        out = Book().bookgen_api_spec()
    elif op == "mdclasses":
        out = modifiedBook().bookgen_api_spec()
    click.echo(out)
    if output:
        with open(output, "w") as f:
            f.write(out)
        click.echo(f"[saved to {output}]")


jsctl.add_command(login)
jsctl.add_command(publogin)
jsctl.add_command(logout)
jsctl.add_command(edit)
jsctl.add_command(ls)
jsctl.add_command(clear)
jsctl.add_command(reset)
jsctl.add_command(script)
jsctl.add_command(studio)
jsctl.add_command(booktool)
cmd_tree_builder(extract_api_tree())
cmd_tree_builder(extract_api_tree()["jac"], group_func=jac)


def main():
    jsctl()


if __name__ == "__main__":
    main()
