"""
Sentinel api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.utils.id_list import IdList
from jaseci.prim.sentinel import Sentinel
from jaseci.utils.utils import b64decode_str
import uuid


class SentinelApi:
    """
    Sentinel APIs

    A sentinel is a unit in Jaseci that represents the organization and management of
    a collection of architypes and walkers. In a sense, you can think of a sentinel
    as a complete Jac implementation of a program or API application. Though its the
    case that many sentinels can be interchangeably across any set of graphs, most
    use cases will typically be a single sentinel shared by all users and managed by an
    admin(s), or each users maintaining a single sentinel customized for their
    individual needs. Many novel usage models are possible, but I'd point the beginner
    to the model most analogous to typical server side software development to start
    with. This model would be to have a single admin account responsible for updating
    a single sentinel that all users would share for their individual graphs. This
    model is achieved through using \\texttt{sentinel_register},
    \\texttt{sentinel_active_global}, and \\texttt{global_sentinel_set}.
    """

    def __init__(self):
        self.active_snt_id = None
        self.sentinel_ids = IdList(self)

    @Interface.private_api(cli_args=["code"])
    def sentinel_register(
        self,
        name: str = "default",
        code: str = "",
        code_dir: str = "./",
        opt_level: int = 4,
        mode: str = "default",
        encoded: bool = False,
        auto_run: str = "init",
        auto_run_ctx: dict = {},
        auto_create_graph: bool = True,
        set_active: bool = True,
    ):
        """
        Create blank or code loaded sentinel and return object
        Auto_run is the walker to execute on register (assumes active graph
        is selected)
        """
        snt = self.sentinel_ids.get_obj_by_name(name, silent=True)
        new_gph = None

        if not snt:
            snt = Sentinel(m_id=self._m_id, h=self._h, name=name)
            self.sentinel_ids.add_obj(snt)
            if auto_create_graph:
                new_gph = self.graph_create(set_active=set_active)
        if code:
            self.sentinel_set(
                code=code,
                code_dir=code_dir,
                encoded=encoded,
                snt=snt,
                mode=mode,
                opt_level=opt_level,
            )
            if not snt.is_active:
                return {
                    "response": "Error in jac code",
                    "errors": snt.errors + snt.runtime_errors,
                    "success": False,
                }
        self.attempt_auto_run(sent=snt, walk_name=auto_run, ctx=auto_run_ctx)
        if set_active:
            self.sentinel_active_set(snt)
        self.extract_snt_aliases(snt)
        if new_gph:
            return [snt.serialize(), new_gph]
        return [snt.serialize()]

    @Interface.private_api()
    def sentinel_pull(self, set_active: bool = True, on_demand: bool = True):
        """
        Copies global sentinel to local master
        """
        glob_id = self._h.get_glob("GLOB_SENTINEL")
        if not glob_id:
            return {"response": "No global sentinel is available!", "success": False}
        g_snt = self._h.get_obj(self._m_id, glob_id).duplicate()

        snt = self.sentinel_ids.get_obj_by_name(g_snt.name, silent=True)
        if not snt:
            snt = Sentinel(m_id=self._m_id, h=self._h, name=g_snt.name)
            self.sentinel_ids.add_obj(snt)
        elif on_demand and snt.is_active:
            return {"response": f"{snt} already active!", "success": True}
        if set_active:
            self.sentinel_active_set(snt)
        return self.sentinel_set(code=g_snt.code_ir, snt=snt, mode="ir")

    @Interface.private_api()
    def sentinel_get(
        self, snt: Sentinel = None, mode: str = "default", detailed: bool = False
    ):
        """
        Get a sentinel rendered with specific mode
        Valid modes: {default, code, ir, }
        """
        if mode == "code":
            return snt._jac_ast.get_text()
        elif mode == "ir":
            return snt.ir_dict()
        else:
            return snt.serialize(detailed=detailed)

    @Interface.private_api(cli_args=["code"])
    def sentinel_set(
        self,
        code: str,
        code_dir: str = "./",
        opt_level: int = 4,
        encoded: bool = False,
        snt: Sentinel = None,
        mode: str = "default",
    ):
        """
        Set code/ir for a sentinel, only replaces walkers/archs in sentinel
        Valid modes: {code, ir, }
        """
        if encoded:
            code = b64decode_str(code)
        if mode not in ["code", "default", "ir"]:
            return {"response": f"Invalid mode to set {snt}", "success": False}
        snt.register_code(code, dir=code_dir, mode=mode, opt_level=opt_level)
        snt.propagate_access()

        if snt.is_active:
            self.extract_snt_aliases(snt)
            return {"response": f"{snt} registered and active!", "success": True}
        else:
            return {
                "response": f"{snt} code issues encountered!",
                "success": False,
                "errors": snt.errors + snt.runtime_errors,
            }

    @Interface.private_api()
    def sentinel_list(self, detailed: bool = False):
        """
        Provide complete list of all sentinel objects
        """
        snts = []
        for i in self.sentinel_ids.obj_list():
            snts.append(i.serialize(detailed=detailed))
        return snts

    @Interface.private_api()
    def sentinel_test(
        self,
        snt: Sentinel = None,
        single: str = "",
        detailed: bool = False,
        profiling: bool = False,
    ):
        """
        Run battery of test cases within sentinel and provide result
        """
        if not len(single):
            single = None
        return snt.run_tests(specific=single, profiling=profiling, detailed=detailed)

    @Interface.private_api(cli_args=["snt"])
    def sentinel_active_set(self, snt: Sentinel):
        """
        Sets the default sentinel master should use
        """
        self.active_snt_id = snt.jid
        self.alias_register("active:sentinel", snt.jid)
        return [f"Sentinel {snt.id} set as default"]

    @Interface.private_api()
    def sentinel_active_unset(self):
        """
        Unsets the default sentinel master should use
        """
        self.active_snt_id = None
        self.alias_delete("active:sentinel")
        return ["Default sentinel unset"]

    @Interface.private_api()
    def sentinel_active_global(
        self,
        auto_run: str = "",
        auto_run_ctx: dict = {},
        auto_create_graph: bool = False,
        detailed: bool = False,
    ):
        """
        Sets the default master sentinel to the global sentinel
        Exclusive OR with pull strategy
        """
        ret = {"success": False, "sentinel": None}
        glob_id = self._h.get_glob("GLOB_SENTINEL")
        if not glob_id:
            ret["response"] = "No global sentinel is available!"
        else:
            self.active_snt_id = "global"  # Resolved in interface
            self.alias_register("active:sentinel", glob_id)
            sent = self._h.get_obj(self._m_id, glob_id)
            if auto_create_graph:
                ret["graph_created"] = self.graph_create(set_active=True)
            auto_run_ret = self.attempt_auto_run(
                sent=sent, walk_name=auto_run, ctx=auto_run_ctx
            )
            if auto_run_ret:
                ret["auto_run_result"] = auto_run_ret
            ret["sentinel"] = sent.serialize(detailed=detailed)
            ret["success"] = True
            ret["response"] = f"Global sentinel {glob_id} set as default"
        return ret

    @Interface.private_api()
    def sentinel_active_get(self, detailed: bool = False):
        """
        Returns the default sentinel master is using
        """
        id = self.active_snt_id
        if id == "global":
            id = self._h.get_glob("GLOB_SENTINEL")
        if not id:
            return {"response": "No default sentinel is selected!", "success": False}
        else:
            default = self._h.get_obj(self._m_id, id)
            return default.serialize(detailed=detailed)

    @Interface.private_api(cli_args=["snt"])
    def sentinel_delete(self, snt: Sentinel):
        """
        Permanently delete sentinel with given id
        """
        self.remove_snt_aliases(snt)
        if self.active_snt_id == snt.jid:
            self.sentinel_active_unset()
        self.sentinel_ids.destroy_obj(snt)
        return [f"Sentinel {snt.id} successfully deleted"]

    def active_snt(self):
        sid = (
            self._h.get_glob("GLOB_SENTINEL")
            if self.active_snt_id == "global"
            else self.active_snt_id
        )
        return self._h.get_obj(self._m_id, sid) if sid is not None else None

    def attempt_auto_run(self, sent: Sentinel, walk_name, ctx):
        if (
            sent.arch_ids.has_obj_by_name(walk_name, kind="walker")
            and self.active_gph_id
        ):
            nd = self._h.get_obj(self._m_id, self.active_gph_id)
            return self.walker_run(name=walk_name, nd=nd, ctx=ctx, snt=sent)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.sentinel_ids.obj_list():
            i.destroy()
