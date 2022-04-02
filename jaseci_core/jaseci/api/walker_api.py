"""
Walker api functions as a mixin
"""
from jaseci.api.interface import interface
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str
from jaseci.utils.id_list import id_list


class walker_api():
    """
    Walker APIs
    """

    def __init__(self):
        self.spawned_walker_ids = id_list(self)

    @interface.public_api(cli_args=['wlk'])
    def walker_summon(self, key: str, wlk: walker, nd: node,
                      ctx: dict = {}, global_sync: bool = True):
        """
        Public api for running walkers, namespace key must be provided
        along with the walker id and node id
        """
        if(key not in wlk.namespace_keys().values()):
            return self.bad_walk_response(
                ['Not authorized to execute this walker'])
        if(global_sync):  # Test needed
            self.sync_walker_from_global_sent(wlk)
        walk = wlk.duplicate()
        walk.refresh()
        walk.prime(nd, prime_ctx=ctx)
        res = walk.run()
        walk.destroy()
        return res

    @interface.private_api(cli_args=['code'])
    def walker_register(self, snt: sentinel = None,
                        code: str = '', encoded: bool = False):
        """
        Create blank or code loaded walker and return object
        """
        if (encoded):
            code = b64decode_str(code)
        walk = snt.register_walker(code)
        if(walk):
            self.extract_wlk_aliases(snt, walk)
            return walk.serialize()
        else:
            return [f'Walker not created, invalid code!']

    @interface.private_api(cli_args=['wlk'])
    def walker_get(self, wlk: walker, mode: str = 'default',
                   detailed: bool = False):
        """
        Get a walker rendered with specific mode
        Valid modes: {default, code, ir, keys, }
        """
        if(mode == 'code'):
            return wlk._jac_ast.get_text()
        elif(mode == 'ir'):
            return wlk.ir_dict()
        elif(mode == 'keys'):
            return wlk.namespace_keys()
        else:
            return wlk.serialize(detailed=detailed)

    @interface.private_api(cli_args=['wlk'])
    def walker_set(self, wlk: walker, code: str,
                   mode: str = 'default'):
        """
        Set code/ir for a walker
        Valid modes: {code, ir, }
        """
        if(mode == 'code' or mode == 'default'):
            wlk.register(code)
        elif(mode == 'ir'):
            wlk.apply_ir(code)
        else:
            return [f'Invalid mode to set {wlk}']
        if(wlk.is_active):
            return [f'{wlk} registered and active!']
        else:
            return [f'{wlk} code issues encountered!']

    @interface.private_api()
    def walker_list(self, snt: sentinel = None, detailed: bool = False):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @interface.private_api(cli_args=['wlk'])
    def walker_delete(self, wlk: walker, snt: sentinel = None):
        """
        Permanently delete walker with given id
        """
        self.remove_wlk_aliases(snt, wlk)
        wlkid = wlk.id
        snt.walker_ids.destroy_obj(wlk)
        return [f'Walker {wlkid} successfully deleted']

    @interface.private_api(cli_args=['name'])
    def walker_spawn_create(self, name: str, snt: sentinel = None):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.spawn_walker(name, caller=self)
        if(wlk):
            if(self.spawned_walker_ids.has_obj_by_name(name)):
                self.spawned_walker_ids.destroy_obj_by_name(name)
            self.spawned_walker_ids.add_obj(wlk)
            self.alias_register(f'spawned:walker:{name}', wlk.jid)
            return wlk.serialize()
        else:
            return [f'Walker not found!']

    @interface.private_api(cli_args=['name'])
    def walker_spawn_delete(self, name: str):
        """
        Delete instance of walker
        """
        if(self.spawned_walker_ids.has_obj_by_name(name)):
            self.spawned_walker_ids.destroy_obj_by_name(name)
            self.alias_delete(f'spawned:walker:{name}')
            return [f'Walker {name} deteled!']
        else:
            return [f'Walker {name} not found!']

    @interface.private_api()
    def walker_spawn_list(self, detailed: bool = False):
        """
        List walkers spawned by master
        """
        walks = []
        for i in self.spawned_walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @interface.private_api(cli_args=['wlk'])
    def walker_prime(self, wlk: walker, nd: node = None, ctx: dict = {}):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx)
        return [f'Walker primed on node {nd.id}']

    @interface.private_api(cli_args=['wlk'])
    def walker_execute(self, wlk: walker, prime: node = None,
                       ctx: dict = {}, profiling: bool = False):
        """
        Executes walker (assumes walker is primed)
        """
        if(prime):
            self.walker_prime(wlk=wlk, nd=prime, ctx=ctx)
        return wlk.run(profiling=profiling)

    @interface.private_api(cli_args=['name'])
    def walker_run(self, name: str, nd: node = None, ctx: dict = {},
                   snt: sentinel = None, profiling: bool = False):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        wlk = snt.spawn_walker(name, caller=self)
        if(not wlk):
            return self.bad_walk_response([f'Walker {name} not found!'])
        res = self.walker_execute(
            wlk=wlk, prime=nd, ctx=ctx, profiling=profiling)
        wlk.destroy()
        return res

    @interface.private_api(cli_args=['name'], url_args=['name'])
    def wapi(self, name: str, nd: node = None, ctx: dict = {},
             snt: sentinel = None, profiling: bool = False):
        """
        Walker individual APIs
        """
        return self.walker_run(name, nd, ctx, snt, profiling)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.spawned_walker_ids.obj_list():
            i.destroy()

    def bad_walk_response(self, errors=list()):
        return {'report': [], 'success': False, 'errors': errors}
