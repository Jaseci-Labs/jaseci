"""
Legacy Master api function as a mixin, should be Deprecated
"""
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.element import element
from jaseci.utils.utils import logger
import base64


class legacy_api():
    """
    APIs that should be deprecated
    """

    def api_load_app(self, name: str, code: str, encoded: bool = False):
        """
        Short for api_load_application
        """
        return self.api_load_application(name, code, encoded)

    def api_load_application(self, name: str, code: str,
                             encoded: bool = True):
        """
        Get or create then return application sentinel and graph pairing
        Code must be encoded in base64
        """
        snt = self.sentinel_ids.get_obj_by_name(name, True)
        gph = self.graph_ids.get_obj_by_name(name, True)
        if (not snt):
            self.api_create_sentinel(name)
            snt = self.sentinel_ids.get_obj_by_name(name)
        if (not gph):
            self.api_create_graph(name)
            gph = self.graph_ids.get_obj_by_name(name)
        self.api_set_jac(snt, code, encoded)
        return {'sentinel': snt.id.urn, 'graph': gph.id.urn,
                'active': snt.is_active}

    def api_prime_walker(self, wlk: walker, nd: node, ctx: dict = {}):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx)
        return [f'Walker primed on node {nd.id}']

    def api_run_walker(self, wlk: walker):
        """
        Executes walker (assumes walker is primed)
        """
        wlk.run()
        return wlk.report

    def api_prime_run(self, snt: sentinel, name: str,
                      nd: node, ctx: dict = {}):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        return self.api_run(snt, name, nd, ctx)

    def api_create_graph(self, name: str):
        """
        Create a graph instance and return root node graph object
        """
        gph = graph(h=self._h, name=name)
        self.graph_ids.add_obj(gph)
        return gph.serialize()

    def api_create_sentinel(self, name: str):
        """
        Create blank sentinel and return object
        """
        snt = sentinel(h=self._h, name=name, code='# Jac Code')
        self.sentinel_ids.add_obj(snt)
        return snt.serialize()

    def api_list_graph(self, detailed: bool = False):
        """
        Provide complete list of all graph objects (list of root node objects)
        """
        gphs = []
        for i in self.graph_ids.obj_list():
            gphs.append(i.serialize(detailed=detailed))
        return gphs

    def api_list_walker(self, snt: sentinel, detailed: bool = False):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    def api_list_sentinel(self, detailed: bool = False):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize(detailed=detailed))
        return snts

    def api_delete_graph(self, gph: graph):
        """
        Permanently delete graph with given id
        """
        self.graph_ids.destroy_obj(gph)
        return [f'Graph {gph.id} successfully deleted']

    def api_delete_sentinel(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """
        self.sentinel_ids.destroy_obj(snt)
        return [f'Sentinel {snt.id} successfully deleted']

    def api_get_graph(self, gph: graph, detailed: bool = False,
                      dot: bool = False):
        """
        Return the content of the graph
        """
        if(dot):
            return gph.graph_dot_str()
        else:
            nds = []
            for i in gph.get_all_nodes():
                nds.append(i.serialize(detailed=detailed))
            return nds

    def api_get_object(self, obj: element, detailed: bool = False):
        """
        Return the content of the graph
        """
        return obj.serialize(detailed=detailed)

    def api_get_jac(self, snt: sentinel):
        """
        Get sentinel implementation in form of Jac source code
        """
        return [snt.code]

    def api_set_jac(self, snt: sentinel, code: str, encoded: bool):
        """
        Set sentinel implementation with Jac source code
        """
        # TODO: HOTFIX for mobile jac file
        code = code.replace("take --> node;", "take -->;")
        if (encoded):
            try:
                code = base64.b64decode(code).decode()
                # TODO: HOTFIX for mobile jac file
                code = code.replace("take --> node;", "take -->;")
            except UnicodeDecodeError:
                logger.error(
                    f'Code encoding invalid for Sentinel {snt.id}!')
                return [f'Code encoding invalid for Sentinel {snt.id}!']
        # TODO: HOTFIX to force recompile jac code everytime
        if (snt.code == code and snt.is_active and False):
            return [f'Sentinel {snt.id} already registered and active!']
        else:
            snt.code = code
            snt.register_code()
            snt.save()
            if(snt.is_active):
                return [f'Sentinel {snt.id} registered and active!']
            else:
                return [f'Sentinel {snt.id} code issues encountered!']

    def api_spawn_walker(self, snt: sentinel, name: str):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.spawn(name)
        if(wlk):
            return wlk.serialize()
        else:
            return [f'Walker not found!']

    def api_unspawn(self, wlk: walker):
        """
        Delete instance of walker (not implemented yet)
        """

        return []

    def api_run(self, snt: sentinel, name: str,
                nd: node, ctx: dict = {}):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        wlk = snt.spawn(name)
        if(not wlk):
            return [f'Walker {name} not found!']
        wlk.prime(nd, prime_ctx=ctx)
        res = self.api_run_walker(wlk)
        wlk.destroy()
        return res

    def api_get_node_context(self, nd: node, ctx: list):
        """
        Returns value a given node
        """
        ret = {}
        nd_ctx = nd.serialize(detailed=True)['context']
        if(ctx):
            for i in nd_ctx.keys():
                if i in ctx:
                    ret[i] = nd_ctx[i]
        return ret

    def api_set_node_context(self, snt: sentinel, nd: node, ctx: dict):
        """
        Assigns values to member variables of a given node using ctx object
        """
        nd.set_context(
            ctx=ctx, arch=snt.arch_ids.get_obj_by_name('node.'+nd.kind).run())
        return nd.serialize()

    def api_create_alias(self, name: str, value: str):
        """
        Creates a string to string alias to be used by client
        """
        if(name in self.alias_map):
            return [f'Aliase {name} already created, please delete first']
        self.alias_map[name] = value
        return [f"Alias from '{name}' to '{value}' created!"]

    def api_list_alias(self):
        """
        List all string to string alias that client can use
        """
        return self.alias_map

    def api_delete_alias(self, name: str = None, all: bool = False):
        """
        Remove string to string alias that client can use
        """
        if(all):
            n = len(self.alias_map.keys())
            self.alias_map = {}
            return [f'All {n} aliases deleted']
        elif(name):
            if(name in self.alias_map.keys()):
                del self.alias_map[name]
                return [f'Alias {name} successfully deleted']
            else:
                return [f'Alias {name} not present']
        return ['Please enter alias to delete or specify all']
