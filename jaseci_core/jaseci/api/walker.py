"""
Walker api functions as a mixin
"""
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel


class walker_api():
    """
    Walker APIs
    """

    def api_walker_create(self, code: str = '', encoded: bool = False):
        """
        Create blank or code loaded walker and return object
        """

    def api_walker_list(self, detailed: bool = False, snt: sentinel = None):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    def api_walker_delete(self, snt: sentinel):
        """
        Permanently delete sentinel with given id
        """

    def api_walker_code_get(self, snt: sentinel = None):
        """
        Get sentinel implementation in form of Jac source code
        """

    def api_walker_code_set(self, code: str, snt: sentinel = None,
                            encoded: bool = False):
        """
        Set sentinel implementation with Jac source code
        """

    def api_walker_spawn(self, name: str, snt: sentinel = None):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.spawn(name)
        if(wlk):
            return wlk.serialize()
        else:
            return [f'Walker not found!']

    def api_walker_unspawn(self, wlk: walker):
        """
        Delete instance of walker (not implemented yet)
        """

        return []

    def api_walker_prime(self, wlk: walker, nd: node = None, ctx: dict = {}):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx)
        return [f'Walker primed on node {nd.id}']

    def api_walker_run(self, wlk: walker):
        """
        Executes walker (assumes walker is primed)
        """
        wlk.run()
        return wlk.report

    def api_walker_primerun(self, name: str, nd: node = None, ctx: dict = {},
                            snt: sentinel = None):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        wlk = snt.spawn(name)
        if(not wlk):
            return [f'Walker {name} not found!']
        wlk.prime(nd, prime_ctx=ctx)
        res = self.api_walker_run(wlk)
        wlk.destroy()
        return res
