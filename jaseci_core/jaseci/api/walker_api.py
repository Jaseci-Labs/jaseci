"""
Walker api functions as a mixin
"""
from jaseci.api.interface import interface
from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str
from jaseci.utils.id_list import id_list


class walker_api:
    """
    Walker APIs

    The walker set of APIs are used for execution and management of walkers. Walkers
    are the primary entry points for running Jac programs. The
    primary API used to run walkers is \\textbf{walker_run}. There are a number of
    variations on this API that enable the invocation of walkers with various
    semantics.
    """

    def __init__(self):
        self.spawned_walker_ids = id_list(self)
        self.yielded_walkers_ids = id_list(self)

    @interface.private_api(cli_args=["code"])
    def walker_register(
        self, snt: sentinel = None, code: str = "", encoded: bool = False
    ):
        """
        Allows for the specific parsing and registering of individual walkers.

        Though the common case is to register entire sentinels, a user can also
        register individual walkers one at a time. This API accepts code for a single
        walker (i.e., \\lstinline\\{walker \\{...\\}\\}).
        """
        if encoded:
            code = b64decode_str(code)
        walk = snt.register_walker(code)
        if walk:
            self.extract_wlk_aliases(snt, walk)
            return walk.serialize()
        else:
            return ["Walker not created, invalid code!"]

    @interface.private_api(cli_args=["wlk"])
    def walker_get(self, wlk: walker, mode: str = "default", detailed: bool = False):
        """
        Get a walker rendered with specific mode
        Valid modes: {default, code, ir, keys, }
        """
        if mode == "code":
            return wlk._jac_ast.get_text()
        elif mode == "ir":
            return wlk.ir_dict()
        elif mode == "keys":
            return wlk.namespace_keys()
        else:
            return wlk.serialize(detailed=detailed)

    @interface.private_api(cli_args=["wlk"])
    def walker_set(self, wlk: walker, code: str, mode: str = "default"):
        """
        Set code/ir for a walker
        Valid modes: {code, ir, }
        """
        if mode == "code" or mode == "default":
            wlk.register(code)
        elif mode == "ir":
            wlk.apply_ir(code)
        else:
            return [f"Invalid mode to set {wlk}"]
        if wlk.is_active:
            return [f"{wlk} registered and active!"]
        else:
            return [f"{wlk} code issues encountered!"]

    @interface.private_api()
    def walker_list(self, snt: sentinel = None, detailed: bool = False):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @interface.private_api(cli_args=["wlk"])
    def walker_delete(self, wlk: walker, snt: sentinel = None):
        """
        Permanently delete walker with given id
        """
        self.remove_wlk_aliases(snt, wlk)
        wlkid = wlk.jid
        ret = {"success": True, "response": f"Walker {wlkid} successfully deleted"}
        if wlk.jid in snt.walker_ids:
            snt.walker_ids.destroy_obj(wlk)
        else:
            ret = {"success": False, "response": f"Walker {wlkid} not found!"}
        return ret

    @interface.private_api(cli_args=["name"])
    def walker_spawn_create(self, name: str, snt: sentinel = None):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.spawn_walker(name, caller=self)
        if wlk:
            if self.spawned_walker_ids.has_obj_by_name(name):
                self.spawned_walker_ids.destroy_obj_by_name(name)
            self.spawned_walker_ids.add_obj(wlk)
            self.alias_register(f"spawned:walker:{name}", wlk.jid)
            return wlk.serialize()
        else:
            return ["Walker not found!"]

    @interface.private_api()
    def walker_spawn_list(self, detailed: bool = False):
        """
        List walkers spawned by master
        """
        walks = []
        for i in self.spawned_walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @interface.private_api(cli_args=["name"])
    def walker_spawn_delete(self, name: str):
        """
        Delete instance of walker
        """
        if self.spawned_walker_ids.has_obj_by_name(name):
            self.spawned_walker_ids.destroy_obj_by_name(name)
            self.alias_delete(f"spawned:walker:{name}")
            return [f"Walker {name} deteled!"]
        else:
            return [f"Walker {name} not found!"]

    @interface.private_api()
    def walker_spawn_clear(self):
        """
        Delete instance of walker
        """
        ret = {"success": True}
        count = len(self.spawned_walker_ids)
        for i in self.spawned_walker_ids.obj_list():
            self.spawned_walker_ids.destroy_obj(i)
        ret["response"] = f"All {count} spawned walkers destroyed."
        return ret

    @interface.private_api()
    def walker_yield_list(self, detailed: bool = False):
        """
        List walkers spawned by master
        """
        walks = []
        for i in self.yielded_walkers_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @interface.private_api(cli_args=["name"])
    def walker_yield_delete(self, name: str):
        """
        Delete instance of walker
        """
        ret = {"success": True}
        if self.yielded_walkers_ids.has_obj_by_name(name):
            self.yielded_walkers_ids.destroy_obj_by_name(name)
            ret["response"] = f"Walker {name} deteled!"
        else:
            ret["success"] = False
            ret["response"] = f"Walker {name} not found!"
        return ret

    @interface.private_api()
    def walker_yield_clear(self):
        """
        Delete instance of walker
        """
        ret = {"success": True}
        count = len(self.yielded_walkers_ids)
        for i in self.yielded_walkers_ids.obj_list():
            self.yielded_walkers_ids.destroy_obj(i)
        ret["response"] = f"All {count} yielded walkers destroyed."
        return ret

    @interface.private_api(cli_args=["wlk"])
    def walker_prime(
        self, wlk: walker, nd: node = None, ctx: dict = {}, _req_ctx: dict = {}
    ):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx, request_ctx=_req_ctx)
        return [f"Walker primed on node {nd.id}"]

    @interface.private_api(cli_args=["wlk"])
    def walker_execute(
        self,
        wlk: walker,
        prime: node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        profiling: bool = False,
    ):
        """
        Executes walker (assumes walker is primed)
        """
        return wlk.run(
            start_node=prime, prime_ctx=ctx, request_ctx=_req_ctx, profiling=profiling
        )

    @interface.private_api(cli_args=["name"])
    def walker_run(
        self,
        name: str,
        nd: node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        snt: sentinel = None,
        profiling: bool = False,
    ):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        wlk = self.yielded_walkers_ids.get_obj_by_name(name, silent=True)
        if wlk is None:
            wlk = snt.spawn_walker(name, caller=self)
        if wlk is None:
            return self.bad_walk_response([f"Walker {name} not found!"])
        res = self.walker_execute(
            wlk=wlk, prime=nd, ctx=ctx, _req_ctx=_req_ctx, profiling=profiling
        )
        wlk.register_yield_or_destroy(self.yielded_walkers_ids)
        return res

    @interface.private_api(cli_args=["name"], url_args=["name"])
    def wapi(
        self,
        name: str,
        nd: node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        snt: sentinel = None,
        profiling: bool = False,
    ):
        """
        Walker individual APIs
        """
        return self.walker_run(name, nd, ctx, _req_ctx, snt, profiling)

    @interface.public_api(cli_args=["wlk"])
    def walker_summon(
        self,
        key: str,
        wlk: walker,
        nd: node,
        ctx: dict = {},
        _req_ctx: dict = {},
        global_sync: bool = True,
    ):
        """
        Public api for running walkers, namespace key must be provided
        along with the walker id and node id
        """
        if key not in wlk.namespace_keys().values():
            return self.bad_walk_response(["Not authorized to execute this walker"])
        if global_sync:
            self.sync_walker_from_global_sent(wlk)

        walk = wlk.duplicate()
        walk.refresh()
        res = self.walker_execute(
            wlk=walk, prime=nd, ctx=ctx, _req_ctx=_req_ctx, profiling=False
        )
        walk.destroy()
        return res

    @interface.public_api(url_args=["nd", "wlk"], allowed_methods=["post", "get"])
    def walker_callback(
        self,
        nd: node,
        wlk: walker,
        key: str,
        ctx: dict = {},
        _req_ctx: dict = {},
        global_sync: bool = True,
    ):
        """
        Public api for running walkers, namespace key must be provided
        along with the walker id and node id
        """

        if key not in wlk.namespace_keys().values():
            return self.bad_walk_response(["Not authorized to execute this walker"])
        if global_sync:
            self.sync_walker_from_global_sent(wlk)

        walk = wlk.duplicate()
        walk.refresh()
        res = self.walker_execute(
            wlk=walk, prime=nd, ctx=ctx, _req_ctx=_req_ctx, profiling=False
        )
        walk.destroy()
        return res

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.spawned_walker_ids.obj_list():
            i.destroy()

    def bad_walk_response(self, errors=list()):
        return {"report": [], "success": False, "errors": errors}
