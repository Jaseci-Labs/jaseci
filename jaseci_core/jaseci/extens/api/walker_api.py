"""
Walker api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.prim.walker import Walker
from jaseci.prim.node import Node
from jaseci.prim.sentinel import Sentinel
from jaseci.utils.id_list import IdList


class WalkerApi:
    """
    Walker APIs

    The walker set of APIs are used for execution and management of walkers. Walkers
    are the primary entry points for running Jac programs. The
    primary API used to run walkers is \\textbf{walker_run}. There are a number of
    variations on this API that enable the invocation of walkers with various
    semantics.
    """

    def __init__(self):
        self.spawned_walker_ids = IdList(self)
        self.yielded_walkers_ids = IdList(self)
        self.reset_profiling(False)

    def reset_profiling(self, profiling):
        self._profiling = profiling
        self._jac_profile = {}

    @Interface.private_api(cli_args=["wlk"])
    def walker_get(self, wlk: Walker, mode: str = "default", detailed: bool = False):
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

    @Interface.private_api()
    def walker_total(self, snt: Sentinel = None, detailed: bool = False):
        """
        Get total walkers known to sentinel
        """
        objects = snt.arch_ids.obj_list()
        walker_objects = list(filter(lambda obj: obj.kind == "walker", objects))
        return len(walker_objects)

    @Interface.private_api()
    def walker_list(self, snt: Sentinel = None, detailed: bool = False):
        """
        List walkers known to sentinel
        """
        walks = []
        for i in snt.arch_ids.obj_list():
            if i.kind == "walker":
                walks.append(i.serialize(detailed=detailed))
        return walks

    @Interface.private_api(cli_args=["name"])
    def walker_spawn_create(self, name: str, snt: Sentinel = None):
        """
        Creates new instance of walker and returns new walker object
        """
        wlk = snt.run_architype(name=name, kind="walker", caller=self, is_async=False)
        wlk.make_persistent()
        if wlk:
            if self.spawned_walker_ids.has_obj_by_name(name):
                self.spawned_walker_ids.destroy_obj_by_name(name)
            self.spawned_walker_ids.add_obj(wlk)
            self.alias_register(f"spawned:walker:{name}", wlk.jid)
            return wlk.serialize()
        else:
            return ["Walker not found!"]

    @Interface.private_api()
    def walker_spawn_list(self, detailed: bool = False):
        """
        List walkers spawned by master
        """
        walks = []
        for i in self.spawned_walker_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @Interface.private_api(cli_args=["name"])
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

    @Interface.private_api()
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

    @Interface.private_api()
    def walker_yield_list(self, detailed: bool = False):
        """
        List walkers spawned by master
        """
        walks = []
        for i in self.yielded_walkers_ids.obj_list():
            walks.append(i.serialize(detailed=detailed))
        return walks

    @Interface.private_api(cli_args=["name"])
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

    @Interface.private_api()
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

    @Interface.private_api(cli_args=["wlk"])
    def walker_prime(
        self, wlk: Walker, nd: Node = None, ctx: dict = {}, _req_ctx: dict = {}
    ):
        """
        Assigns walker to a graph node and primes walker for execution
        """
        wlk.prime(nd, prime_ctx=ctx, request_ctx=_req_ctx)
        return [f"Walker primed on node {nd.id}"]

    @Interface.private_api(cli_args=["wlk"])
    def walker_execute(
        self,
        wlk: Walker,
        prime: Node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        profiling: bool = False,
    ):
        """
        Executes walker (assumes walker is primed)
        """
        self.reset_profiling(profiling)
        return wlk.run(
            start_node=prime, prime_ctx=ctx, request_ctx=_req_ctx, profiling=profiling
        )

    @Interface.private_api(cli_args=["wlk"])
    def walker_step(self, wlk: Walker, detailed: bool = False):
        """
        Executes walker (assumes walker is primed)
        """
        wlk.step()
        ret = {
            "current_node": wlk.current_node.serialize(detailed=detailed),
            "next_node_ids": wlk.next_node_ids,
            "walker_context": wlk.serialize(detailed=detailed)["context"],
            "walker_report": wlk.report,
            "profile": wlk.profile,
        }
        return ret

    @Interface.private_api(cli_args=["name"])
    def walker_run(
        self,
        name: str,
        nd: Node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        snt: Sentinel = None,
        profiling: bool = False,
        is_async: bool = None,
    ):
        """
        Creates walker instance, primes walker on node, executes walker,
        reports results, and cleans up walker instance.
        """
        self.reset_profiling(profiling)
        wlk = self.yielded_walkers_ids.get_obj_by_name(name, silent=True)
        if wlk is None:
            wlk = snt.run_architype(
                name=name, kind="walker", caller=self, is_async=is_async
            )
        if wlk is None:
            return self.bad_walk_response([f"Walker {name} not found!"])
        res = self.walker_execute(
            wlk=wlk, prime=nd, ctx=ctx, _req_ctx=_req_ctx, profiling=profiling
        )
        wlk.register_yield_or_destroy(self.yielded_walkers_ids)
        return res

    @Interface.private_api(cli_args=["name"], url_args=["name"])
    def wapi(
        self,
        name: str,
        nd: Node = None,
        ctx: dict = {},
        _req_ctx: dict = {},
        snt: Sentinel = None,
        profiling: bool = False,
    ):
        """
        Walker individual APIs
        """
        self.reset_profiling(profiling)
        return self.walker_run(name, nd, ctx, _req_ctx, snt, profiling)

    @Interface.public_api(cli_args=["wlk"])
    def walker_summon(
        self,
        key: str,
        wlk: Walker,
        nd: Node,
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
            # Deprecated Walkers are always synced with sentinel now
            pass

        walk = wlk.duplicate()
        res = self.walker_execute(
            wlk=walk, prime=nd, ctx=ctx, _req_ctx=_req_ctx, profiling=False
        )
        walk.destroy()
        return res

    @Interface.public_api(url_args=["nd", "wlk"], allowed_methods=["post", "get"])
    def walker_callback(
        self,
        nd: Node,
        wlk: Walker,
        key: str,
        ctx: dict = {},
        _req_ctx: dict = {},
        global_sync: bool = True,
    ):
        """
        Public api for running walkers, namespace key must be provided
        along with the walker id and node id
        """

        return self.walker_summon(
            nd=nd,
            wlk=wlk,
            key=key,
            ctx=ctx,
            _req_ctx=_req_ctx,
            global_sync=global_sync,
        )

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.spawned_walker_ids.obj_list():
            i.destroy()

    def bad_walk_response(self, errors=list()):
        return {"report": [], "success": False, "errors": errors}
