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
from jaseci.master import master as master_class
from jaseci.api.public import public_api
from .ci_app import ci_program

session = {
    "filename": "js.session",
    "master": master_class(h=mem_hook()),
    "mem-only": False
}

connection = {'url': None, 'token': None, 'headers': None}


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
    """Constructs and issues call to remote server"""
    if(api_name.startswith('api_')):
        path = '/jac/'+api_name[4:]
    elif(api_name.startswith('admin_api_')):
        path = '/admin/'+api_name[10:]
    elif(api_name.startswith('public_api_')):
        path = '/public/'+api_name[11:]
    ret = requests.post(connection['url']+path,
                        data=payload,
                        headers=connection['headers'])
    if ret.status_code > 205:
        ret = f"Status Code Error {ret.status_code}"
    else:
        ret = ret.json()
    return ret


def interface_api(api_name, is_public, **kwargs):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    if('code' in kwargs and kwargs['code']):
        if (os.path.isfile(kwargs['code'])):
            with open(kwargs['code'], 'r') as file:
                kwargs['code'] = file.read()
        else:
            click.echo(f"Code file {kwargs['code']} not found!")
            return
    if('ctx' in kwargs):
        kwargs['ctx'] = json.loads(kwargs['ctx'])
    if(connection['token'] and connection['url']):
        out = remote_api_call(kwargs, api_name)
    elif(is_public):
        out = public_api(session['master']._h).general_interface_to_api(
            kwargs, api_name)
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


def extract_api_tree():
    """
    Generates a tree of command group names and function
    signatures in leaves from API function names in Master
    """
    api_funcs = {}
    for i in dir(session['master'])+dir(public_api(None)):
        if (i.startswith('api_') or i.startswith('admin_api_') or
                i.startswith('public_api_')):
            is_public = False
            # Get function names and signatures
            func_str = i[4:] if i.startswith('api_') else i[10:]
            if(func_str[0] == '_'):  # is public api
                func_str = func_str[1:]
                is_public = True
            cmd_groups = func_str.split('_')
            func_sig = session['master'].get_api_signature(
                i) if not is_public else public_api(None).get_api_signature(i)
            func_doc = session['master'].get_api_doc(
                i) if not is_public else public_api(None).get_api_doc(i)

            # Build hierarchy of command groups
            api_root = api_funcs
            for j in cmd_groups:
                if (j not in api_root.keys()):
                    api_root[j] = {}
                api_root = api_root[j]
            api_root['leaf'] = [i, func_sig, is_public, func_doc]
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
        if(p_type != int and p_type != bool):
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
        click.echo(f"Login failed!\n{r.json()}")


@click.command(help="Edit a file")
@click.argument("file", type=str, required=True)
def edit(file):
    ci_program.set_args([file])
    ci_program.run_ci()


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


def all_help(root, out=None, str=""):
    if(out is None):
        out = []
    if('leaf' in root.keys()):
        out.append(str+f'& {root["leaf"][1]} &\n')
        return
    for i in root.keys():
        all_help(root[i], out, str+f'{i} ')
    ret = ''
    for i in out:
        ret += i
    return ret


@click.command(help="Internal dev operations")
@click.argument("op", type=str, default='all_help', required=True)
def dev(op):
    if(op == 'all_help'):
        click.echo(
            f"{all_help(extract_api_tree())}")


cli.add_command(login)
cli.add_command(edit)
cli.add_command(ls)
cli.add_command(dev)
cmd_tree_builder(extract_api_tree())


def main():
    cli()


if __name__ == '__main__':
    main()
