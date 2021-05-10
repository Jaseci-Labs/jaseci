"""
Legacy Master api function as a mixin should be Deprecated
"""
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel


class master_legacy_api():
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
