"""
Sentinel class for Jaseci

Each sentinel has an id, name, timestamp and it's set of walkers.
"""
from jaseci.element.element import Element
from jaseci.utils.utils import logger, ColCodes as Cc
from jaseci.utils.id_list import IdList
from jaseci.jac.ir.jac_code import JacCode, jac_ir_to_ast
from jaseci.jac.interpreter.sentinel_interp import SentinelInterp
from jaseci.actor.walker import Walker
from jaseci.actor.architype import Architype


class Sentinel(Element, JacCode, SentinelInterp):
    """
    Sentinel class for Jaseci

    is_active is used to signify whether sentinel is ready to run walkers, i.e,
    register_code succeeded
    """

    def __init__(self, *args, **kwargs):
        self.version = None
        self.arch_ids = IdList(self)
        self.global_vars = {}
        self.testcases = []
        Element.__init__(self, *args, **kwargs)
        JacCode.__init__(self, code_ir=None)
        SentinelInterp.__init__(self)
        self.load_arch_defaults()

    def load_arch_defaults(self):
        self.arch_ids.add_obj(
            Architype(m_id=self._m_id, h=self._h, name="root", kind="node")
        )
        self.arch_ids.add_obj(
            Architype(m_id=self._m_id, h=self._h, name="generic", kind="node")
        )
        self.arch_ids.add_obj(
            Architype(m_id=self._m_id, h=self._h, name="generic", kind="edge")
        )

    def reset(self):
        """Resets state of sentinel and unregister's code"""
        self.version = None
        self.global_vars = {}
        self.testcases = []
        self.arch_ids.destroy_all()
        self.load_arch_defaults()
        JacCode.reset(self)
        SentinelInterp.reset(self)

    def refresh(self):
        super().refresh()
        self.ir_load()

    def register_code(self, text, dir="./", mode="default"):
        """
        Registers a program (set of walkers and architypes) written in Jac
        """
        self.reset()
        if mode == "ir":
            self.apply_ir(text)
        else:
            self.register(text, dir)
        if self.is_active:
            self.ir_load()
        return self.is_active

    def ir_load(self):
        """
        Load walkers and architypes from IR
        """
        self.run_start(self._jac_ast)

        if self.runtime_errors:
            logger.error(str(f"{self.name}: Runtime problem processing sentinel!"))
            self.is_active = False
        elif not self.arch_ids:
            logger.error(str(f"{self.name}: No walkers nor architypes created!"))
            self.is_active = False
        return self.is_active

    def register_walker(self, code, dir):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, dir=dir, start_rule="walker")
        if not tree:
            return None
        return self.load_walker(tree)

    def register_architype(self, code):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, start_rule="architype")
        if not tree:
            return None
        return self.load_architype(tree)

    def spawn_architype(self, name, kind=None, caller=None):
        """
        Spawns a new architype from registered architypes and adds to
        live walkers
        """
        src_arch = self.arch_ids.get_obj_by_name(name, kind=kind, silent=True)
        if not src_arch:
            logger.error(str(f"{self.name}: Unable to spawn {kind} architype {name}!"))
            return None

        if caller and caller._m_id != src_arch._m_id:
            new_arch = src_arch.duplicate()
            new_arch.set_master(caller._m_id)
            new_arch._jac_ast = src_arch._jac_ast
            if new_arch._jac_ast is None:
                new_arch.refresh()
            return new_arch
        else:
            return src_arch

    def run_architype(self, name, kind=None, caller=None):
        """
        Spawn, run, then destroy architype if m_id's are different
        """
        if caller is None:
            caller = self
        arch = self.spawn_architype(name, kind, caller)
        if arch is None:
            logger.error(
                str(f"{self.name}: Unable to spawn architype " f"{[name, kind]}!")
            )
            return None
        if arch.jid in self.arch_ids:
            return arch.run()
        else:
            ret = arch.run()
            Element.destroy(arch)
            return ret

    def get_arch_for(self, obj):
        """Returns the architype that matches object"""
        ret = self.arch_ids.get_obj_by_name(name=obj.name, kind=obj.kind)
        if ret is None:
            self.rt_error(f"Unable to find architype for {obj.name}, {obj.kind}")
        return ret

    def check_in_arch_context(self, key_name, object):
        """
        Validates a key is present in currently loaded architype of
        a particular instance (helper for expanding node has variables)
        """
        src_arch = self.run_architype(object.name, kind=object.kind)
        return key_name in src_arch.context

    def run_tests(self, detailed=False, silent=False):
        """
        Testcase schema
        testcase = {'title': kid[1].token_text(),
            'graph_ref': None, 'graph_block': None,
            'walker_ref': None, 'spawn_ctx': None,
            'assert_block': None, 'walker_block': None,
            'passed': None}
        """
        from pprint import pformat
        from time import time
        import sys
        import io

        num_failed = 0
        for i in self.testcases:
            screen_out = [sys.stdout, sys.stderr]
            buff_out = [io.StringIO(), io.StringIO()]
            destroy_set = []
            title = i["title"]
            if i["graph_ref"]:
                gph = self.run_architype(i["graph_ref"], kind="graph", caller=self)
            else:
                gph = Architype(
                    m_id=self._m_id,
                    h=self._h,
                    parent=self,
                    code_ir=jac_ir_to_ast(i["graph_block"]),
                )
                destroy_set.append(gph)
                gph = gph.run()
            if i["walker_ref"]:
                wlk = self.run_architype(
                    name=i["walker_ref"], kind="walker", caller=self
                )
            else:
                wlk = Walker(
                    m_id=self._m_id,
                    h=self._h,
                    parent=self,
                    code_ir=jac_ir_to_ast(i["walker_block"]),
                )
                destroy_set.append(wlk)
            wlk.prime(gph)
            if i["spawn_ctx"]:
                self.run_spawn_ctx(jac_ir_to_ast(i["spawn_ctx"]), wlk)

            stime = time()
            try:
                if not silent:
                    print(f"Testing {title}: ", end="")
                sys.stdout, sys.stderr = buff_out[0], buff_out[1]
                wlk.run()
                sys.stdout, sys.stderr = screen_out[0], screen_out[1]
                if i["assert_block"]:
                    wlk._loop_ctrl = None
                    wlk.scope_and_run(
                        jac_ir_to_ast(i["assert_block"]), run_func=wlk.run_code_block
                    )
                i["passed"] = True
                if not silent:
                    print(
                        f"[{Cc.TG}PASSED{Cc.EC} in {Cc.TY}{time()-stime:.2f}s{Cc.EC}]"
                    )
                if detailed and not silent:
                    print("REPORT: " + pformat(wlk.report))
            except Exception as e:
                sys.stdout, sys.stderr = screen_out[0], screen_out[1]
                i["passed"] = False
                num_failed += 1
                if not silent:
                    print(
                        f"[{Cc.TR}FAILED{Cc.EC} in {Cc.TY}{time()-stime:.2f}s{Cc.EC}]"
                    )
                    print(f"{e}")
            for i in destroy_set:  # FIXME: destroy set not complete
                i.destroy()
        num_tests = len(self.testcases)
        summary = {
            "tests": num_tests,
            "passed": num_tests - num_failed,
            "failed": num_failed,
            "success": num_tests and not num_failed,
        }
        if detailed:
            details = []
            for i in self.testcases:
                details.append(
                    {
                        "test": i["title"],
                        "passed": i["passed"],
                        "stdout": buff_out[0].getvalue(),
                        "stderr": buff_out[1].getvalue(),
                    }
                )
            summary["details"] = details
        return summary

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.arch_ids.obj_list():
            i.destroy()
        super().destroy()
