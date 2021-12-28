"""
Command line tool for Jaseci
"""

import click
from click_shell import shell
import os
import pickle
import functools
import json
import requests

from jaseci.utils.mem_hook import mem_hook
from jaseci.utils.utils import copy_func
from jaseci.element.super_master import super_master
from .book_tools import book

session = None
connection = None


def reset_state():
    global session, connection
    session = {
        "filename": "js.session",
        "user": [super_master(h=mem_hook(), name='admin')],
        "mem-only": session["mem-only"] if session is not None else False
    }
    session['master'] = session['user'][0]

    connection = {'url': None, 'token': None, 'headers': None}


reset_state()


def blank_func():
    """No help provided"""
    pass


@shell(prompt='jaseci > ', intro='Starting Jaseci Shell...')
@click.option('--filename', '-f', default="js.session",
              help="Specify filename for session state.")
@click.option('--mem-only', '-m', is_flag=True,
              help="Set true to not save file for session.")
def cli(filename, mem_only):
    """
    The Jaseci Command Line Interface
    """
    session['mem-only'] = mem_only
    session['filename'] = filename if not mem_only else None
    if (not mem_only and os.path.isfile(filename)):
        with open(filename, 'rb') as f:
            session['master'] = pickle.load(f)


def remote_api_call(payload, api_name):
    """
    Constructs and issues call to remote server
    NOTE: Untested
    """
    for i in super_master.all_apis(None):
        if(api_name == '_'.join(i['groups'])):
            if(i in super_master._private_api):
                path = '/jac/'+api_name
            elif(i in super_master._admin_api):
                path = '/admin/'+api_name
            elif(i in super_master._public_api):
                path = '/public/'+api_name
            break
    ret = requests.post(connection['url']+path,
                        json=payload,
                        headers=connection['headers'])
    if ret.status_code > 205:
        ret = f"Status Code Error {ret.status_code}"
    else:
        ret = ret.json()
    return ret


def resolve_none_type(kwargs):
    for i in kwargs.keys():
        if(kwargs[i] == 'None'):
            kwargs[i] = None


def interface_api(api_name, is_public, **kwargs):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    if('code' in kwargs and kwargs['code']):
        if (os.path.isfile(kwargs['code'])):
            with open(kwargs['code'], 'r') as file:
                if(kwargs['name'] == 'default'):
                    kwargs['name'] = kwargs['code']
                kwargs['code'] = file.read()
        else:
            click.echo(f"Code file {kwargs['code']} not found!")
            return
    if('ctx' in kwargs):  # can replace these checs with a dict check
        kwargs['ctx'] = json.loads(kwargs['ctx'])
    if('other_fields' in kwargs):
        kwargs['other_fields'] = json.loads(kwargs['other_fields'])
    resolve_none_type(kwargs)
    if(connection['token'] and connection['url']):
        out = remote_api_call(kwargs, api_name)
    elif(is_public):
        out = session['master'].public_interface_to_api(kwargs, api_name)
    else:
        out = session['master'].general_interface_to_api(kwargs, api_name)
    if(isinstance(out, dict) or isinstance(out, list)):
        out = json.dumps(out, indent=2)
    click.echo(out)
    if('output' in kwargs and kwargs['output']):
        with open(kwargs['output'], 'w') as f:
            f.write(out)
        click.echo(f'[saved to {kwargs["output"]}]')
    if not session['mem-only']:
        with open(session['filename'], 'wb') as f:
            pickle.dump(session['master'], f)

    # api_funcs = {}
    # for i in session['master']._public_api:
    #     if (i.startswith('api_') or i.startswith('admin_api_') or
    #             i.startswith('public_api_')):
    #         is_public = False
    #         # Get function names and signatures
    #         if i.startswith('api_'):
    #             func_str = i[4:]
    #         elif i.startswith('admin_'):
    #             func_str = i[10:]
    #         else:  # is public api
    #             func_str = i[11:]
    #             is_public = True
    #         cmd_groups = func_str.split('_')
    #         func_sig = session['master'].get_api_signature(i)
    #         func_doc = session['master'].get_api_doc(i


def extract_api_tree():
    """
    Generates a tree of command group names and function
    signatures in leaves from API function names in Master
    """
    api_funcs = {}
    for i in session['master'].all_apis():
        # Build hierarchy of command groups
        api_root = api_funcs
        for j in i['groups']:
            if (j not in api_root.keys()):
                api_root[j] = {}
            api_root = api_root[j]
        api_root['leaf'] = ['_'.join(i['groups']), i['sig'],
                            i in session['master']._public_api,  i['doc']]
    return api_funcs


def build_cmd(group_func, func_name, leaf):
    """
    Generates Click function with options for each command
    group and leaf signatures
    leaf is format: [api_name, func_sig, is_public, func_doc]
    """

    f = functools.partial(
        copy_func(interface_api, func_name),
        api_name=leaf[0], is_public=leaf[2])
    f.__name__ = func_name
    f.__doc__ = leaf[3]

    func_sig = leaf[1]
    for i in func_sig.parameters.keys():
        if(i == 'self'):
            continue
        p_default = func_sig.parameters[i].default
        p_type = func_sig.parameters[i].annotation
        if(p_type not in [int, bool, float]):
            p_type = str
        if(p_default is not func_sig.parameters[i].empty):
            f = click.option(
                f'-{i}', default=p_type(p_default), required=False,
                type=p_type)(f)
        else:
            f = click.option(
                f'-{i}', required=True, type=p_type)(f)
    # to file option to dump response to a file
    f = click.option(
        '--output', '-o', default='', required=False, type=str,
        help="Filename to dump output of this command call.")(f)
    return group_func.command()(f)


def cmd_tree_builder(location, group_func=cli, cmd_str=''):
    """
    Generates Click command groups from API tree recursively
    """
    for i in location.keys():
        loc = location[i]
        if ('leaf' in loc):
            build_cmd(group_func, i, loc['leaf'])
            continue
        else:
            f = copy_func(blank_func, i)
            f.__doc__ = f'Group of `{(cmd_str+" "+i).lstrip()}` commands'
            new_func = group_func.group()(f)
        cmd_tree_builder(loc, new_func, cmd_str+' '+i)


@click.command(help="Command to log into live Jaseci server")
@click.argument("url", type=str, required=True)
@click.option('--username', '-u', required=True, prompt=True,
              help="Username to be used for login.")
@click.password_option(help="Password to be used for login.",
                       confirmation_prompt=False)
def login(url, username, password):
    url = url[:-1] if url[-1] == '/' else url
    payload = {'email': username, 'password': password}
    r = requests.post(url+'/user/token/', data=payload).json()
    if('token' in r.keys()):
        connection['token'] = r['token']
        connection['url'] = url
        connection['headers'] = {
            'Authorization': 'token ' + r['token']}
        click.echo("Login successful!")
    else:
        click.echo(f"Login failed!\n{r}")


@click.command(help="Edit a file")
@click.argument("file", type=str, required=True)
def edit(file):
    click.edit(filename=file)


@click.command(help="List relevant files")
@click.option('--all', '-a', is_flag=True,
              help="Flag for listing all files, not just relevant files")
def ls(all):
    for i in os.listdir():
        if(all):
            click.echo(f"{i}")
        else:
            click.echo(f"{i}") if i.endswith(
                '.jac') or i.endswith('.dot') else False


@click.command(help="Clear terminal")
def clear():
    click.clear()


@click.command(help="Reset jsctl (clears state)")
def reset():
    reset_state()
    click.echo(f"Jaseci State Cleared!")


@click.command(help="Internal book generation tools")
@click.argument("op", type=str, default='cheatsheet', required=True)
@click.option('--output', '-o', default='', required=False, type=str,
              help="Filename to dump output of this command call.")
def tool(op, output):
    out = ''
    if(op == 'cheatsheet'):
        out = f"{book().api_cheatsheet(extract_api_tree())}"
    elif(op == 'classes'):
        out = book().api_spec()
    click.echo(out)
    if(output):
        with open(output, 'w') as f:
            f.write(out)
        click.echo(f'[saved to {output}]')


cli.add_command(login)
cli.add_command(edit)
cli.add_command(ls)
cli.add_command(clear)
cli.add_command(reset)
cli.add_command(tool)
cmd_tree_builder(extract_api_tree())


def main():
    cli()


if __name__ == '__main__':
    main()
