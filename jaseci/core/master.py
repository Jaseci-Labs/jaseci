"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""
import base64
from core.element import element
from core.graph.graph import graph
from core.graph.node import node
from core.actor.sentinel import sentinel
from core.actor.walker import walker
from core.utils.id_list import id_list


class master(element):
    """Main class for master functions for user"""

    def __init__(self, email="Anonymous", *args, **kwargs):
        self.graph_ids = id_list(self)
        self.sentinel_ids = id_list(self)
        super().__init__(name=email, kind="Jaseci Master", *args, **kwargs)

    def api_load_application(self, name: str, code: str):
        """
        Get or create then return application sentinel and graph pairing
        Code must be encoded in base64
        """
        # TODO: Do better recompilation here
        self.sentinel_ids.destroy_obj_by_name(name, True)
        snt = None
        # snt = self.sentinel_ids.get_obj_by_name(name, True)
        gph = self.graph_ids.get_obj_by_name(name, True)
        if (not snt):
            self.api_create_sentinel(name)
            snt = self.sentinel_ids.get_obj_by_name(name)
        if (not gph):
            self.api_create_graph(name)
            gph = self.graph_ids.get_obj_by_name(name)
        self.api_set_jac_code(snt, code, True)
        return {'sentinel': snt.id.urn, 'graph': gph.id.urn,
                'active': snt.is_active}

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

    def api_list_graphs(self):
        """
        Provide complete list of all graph objects (list of root node objects)
        """
        gphs = []
        for i in self.graph_ids.obj_list():
            gphs.append(i.serialize())
        return gphs

    def api_list_sentinels(self):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize())
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

    def api_get_jac_code(self, snt: sentinel):
        """
        Get sentinel implementation in form of Jac source code
        """
        return [snt.code]

    def api_set_jac_code(self, snt: sentinel, code: str, encoded: bool):
        """
        Set sentinel implementation with Jac source code
        """
        if (encoded):
            code = base64.b64decode(code).decode()
        if (snt.code == code and snt.is_active):
            return [f'Sentinel {snt.id} already registered and active!']
        else:
            snt.code = code
            return self.api_compile(snt)

    def api_compile(self, snt: sentinel):
        """
        Compile and register sentinel (ready to run if successful)
        """
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

    def api_prime_walker(self, wlk: walker, nd: node, ctx: dict):
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

    def api_prime_run(self, snt: sentinel, name: str, nd: node, ctx: dict):
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

    def api_get_node_context(self, snt: sentinel, nd: node):
        """
        Returns value a given node
        """
        return nd.serialize()

    def api_set_node_context(self, snt: sentinel, nd: node, ctx: dict):
        """
        Assigns values to member variables of a given node using ctx object
        """
        nd.set_context(
            ctx=ctx, arch=snt.arch_ids.get_obj_by_name('node.'+nd.kind).run())
        return nd.serialize()

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list() + self.graph_ids.obj_list():
            i.destroy()
        super().destroy()
