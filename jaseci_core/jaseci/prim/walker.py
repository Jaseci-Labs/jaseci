"""
Walker class for Jaseci

Each walker has an id, name, timestamp and it's parent sentinel.
TODO: Perhaps  I should have walker state (context ids) in mem only with
default hooks to save db read/writes
"""

from jaseci.utils.utils import (
    logger,
    perf_test_start,
    perf_test_stop,
    exc_stack_as_str_list,
)
from jaseci.prim.element import Element
from jaseci.prim.obj_mixins import Anchored
from jaseci.utils.id_list import IdList
from jaseci.jac.machine.machine_state import TryException
from jaseci.jac.interpreter.walker_interp import WalkerInterp
import uuid
import hashlib

from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.task_svc import TaskService
from jaseci.utils.utils import format_jac_profile


class Walker(Element, WalkerInterp, Anchored):
    """Walker class for Jaseci"""

    def __init__(self, is_async=False, **kwargs):
        self.yielded = False
        self.namespaces = []
        self.profile = {}
        # Process state
        self.current_node_id = None
        self.next_node_ids = IdList(self)
        self.destroy_node_ids = IdList(self)
        self.current_step = 0
        self.in_entry_exit = False
        self.step_limit = 10000
        self.is_async = is_async
        self._to_await = False
        if "persist" not in kwargs:  # Default walker persistence to is_async
            kwargs["persist"] = is_async
        Element.__init__(self, **kwargs)
        WalkerInterp.__init__(self)
        Anchored.__init__(self)

    @property
    def current_node(self):
        if not self.current_node_id:
            return None
        elif not self._h.has_obj(self.current_node_id):
            self.current_node_id = None
            return None
        else:
            return self._h.get_obj(self._m_id, self.current_node_id)

    @current_node.setter
    def current_node(self, obj):
        if obj:
            self.current_node_id = obj.jid
        else:
            self.current_node_id = None

    def namespace_keys(self):
        """Return list of md5 keys for namespaces"""
        ret = {}
        for i in self.namespaces:
            ret[i] = hashlib.md5((self._m_id + i).encode()).hexdigest()
        return ret

    def for_queue(self):
        return self.is_async and not (self._to_await)

    def step(self):
        """
        Take single step through program
        if no ast provided, will be generated from code
        """
        if not self.next_node_ids:
            logger.debug(str(f"Walker {self.name} is disengaged"))
            return False
        if self.current_step > self.step_limit:
            logger.error(
                str(
                    f"Walker {self.name} walked too many steps "
                    + f"- {self.step_limit}"
                )
            )
            return False

        self.current_node = self.next_node_ids.pop_first_obj()
        self.run_walker(jac_ast=self.get_architype().get_jac_ast())
        if self.current_step < 200:
            self.log_history("visited", self.current_node.id)
        self.current_step += 1
        self.profile["steps"] = self.current_step
        if self._stopped == "skip":
            self._stopped = None
        if self.next_node_ids:
            logger.debug(
                str(
                    f"Step complete, Walker {self.name} next node: "
                    + f"- {self.next_node_ids.first_obj()}"
                )
            )
            return self.next_node_ids.first_obj()
        else:
            logger.debug(
                str(
                    f"Final step of walker {self.name} complete"
                    + f"- disengaging from {self.current_node}"
                )
            )
            for i in self.destroy_node_ids.obj_list():
                if i.jid == self.current_node_id:
                    self.current_node_id = None
                i.destroy()
                self.destroy_node_ids.remove_obj(i)
            return True

    def prime(self, start_node, prime_ctx=None, request_ctx=None):
        """Place walker on node and get ready to step step"""
        if not self.yielded or not len(self.next_node_ids):  # modus ponens
            self.next_node_ids.add_obj(start_node, push_front=True)
        if prime_ctx:
            for i in prime_ctx.keys():
                self.context[str(i)] = prime_ctx[i]
        self.request_context = request_ctx
        self.profile["steps"] = self.current_step
        logger.debug(str(f"Walker {self.name} primed - {start_node}"))

    def run(self, start_node=None, prime_ctx=None, request_ctx=None, profiling=False):
        """Executes Walker to completion"""
        if self.for_queue() and JsOrc.svc("task").is_running():
            start_node = (
                start_node
                if not (start_node is None)
                else (
                    self.next_node_ids.pop_first_obj() if self.next_node_ids else None
                )
            )

            self._h.commit_all_cache_sync()

            return {
                "is_queued": True,
                "result": JsOrc.svc("task", TaskService).add_queue(
                    self,
                    start_node,
                    prime_ctx or self.context,
                    request_ctx or self.request_context,
                    profiling,
                ),
            }

        if profiling:
            pr = perf_test_start()

        if start_node and (not self.yielded or not len(self.next_node_ids)):
            self.prime(start_node, prime_ctx, request_ctx)
        elif prime_ctx:
            for i in prime_ctx.keys():
                self.context[str(i)] = prime_ctx[i]

        report_ret = {"success": True}
        WalkerInterp.reset(self)
        self.yielded = False

        try:
            while self.step() and not self.yielded:
                pass
        except Exception:
            report_ret["success"] = False
            report_ret["stack_trace"] = exc_stack_as_str_list()

        self.save()

        if not self.report:
            logger.debug(str(f"Walker {self.name} did not have anything to report"))
        report_ret["report"] = self.report
        report_ret["final_node"] = self.current_node_id
        report_ret["yielded"] = self.yielded

        if self.report_status:
            report_ret["status_code"] = self.report_status
        if self.report_custom:
            report_ret["report_custom"] = self.report_custom
        if self.report_file:
            report_ret["report_file"] = self.report_file

        if len(self.runtime_errors):
            report_ret["errors"] = self.runtime_errors
            report_ret["success"] = False
        if len(self.runtime_stack_trace):
            report_ret["stack_trace"] = (
                report_ret.get("stack_trace", []) + self.runtime_stack_trace
            )
        if profiling:
            self.profile["jac"] = format_jac_profile(self.get_master()._jac_profile)
            calls, graph = perf_test_stop(pr)
            self.profile["perf"] = calls
            self.profile["graph"] = graph
            report_ret["profile"] = self.profile

        if self.for_queue():
            return {"is_queued": False, "result": report_ret}

        return report_ret

    def yield_walk(self):
        """Instructs walker to yield (stop walking and keep state)"""
        self.yielded = True

    def log_history(self, name, value):
        """Helper function for logging history of walker's activities"""
        if isinstance(value, Element):
            value = {"type": value.j_type, "id": value.jid}
        if isinstance(value, uuid.UUID):
            value = value.urn
        if name in self.profile.keys():
            self.profile[name].append(value)
        else:
            self.profile[name] = [value]

    def clear_state(self):
        """Clears walker state after report"""
        self.yielded = False
        self.profile = {}
        self.current_step = 0
        self.next_node_ids.remove_all()
        self.ignore_node_ids.remove_all()
        self.destroy_node_ids.remove_all()
        self.current_node = None
        self.context = {}
        WalkerInterp.reset(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        if not self.for_queue() or not JsOrc.svc("task").is_running():
            WalkerInterp.destroy(self)
            super().destroy()

    def register_yield_or_destroy(self, yield_ids):
        """Helper for auto destroying walkers"""
        if not self.yielded:
            if self.jid in yield_ids:
                yield_ids.remove_obj(self)
            self.destroy()
        else:
            yield_ids.add_obj(self, silent=True)

    def save(self):
        """
        Write self through hook to persistent storage
        """
        self._h.save_obj(caller_id=self._m_id, item=self, all_caches=self.is_async)
