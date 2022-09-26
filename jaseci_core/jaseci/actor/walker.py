"""
Walker class for Jaseci

Each walker has an id, name, timestamp and it's parent sentinel.
TODO: Perhaps  I should have walker state (context ids) in mem only with
default hooks to save db read/writes
"""

from jaseci.utils.utils import logger
from jaseci.element.element import Element
from jaseci.element.obj_mixins import Anchored
from jaseci.utils.id_list import IdList
from jaseci.jac.interpreter.walker_interp import WalkerInterp
import uuid
import hashlib
import io
import pstats
import cProfile


class Walker(Element, WalkerInterp, Anchored):
    """Walker class for Jaseci"""

    valid_async = [True, "true"]

    def __init__(self, code_ir=None, **kwargs):
        self.yielded = False
        self.activity_action_ids = IdList(self)
        self.namespaces = []
        self.profile = {}
        # Process state
        self.current_node_id = None
        self.next_node_ids = IdList(self)
        self.ignore_node_ids = IdList(self)
        self.destroy_node_ids = IdList(self)
        self.current_step = 0
        self.in_entry_exit = False
        self.step_limit = 10000
        self._async = False
        Element.__init__(self, **kwargs)
        WalkerInterp.__init__(self)
        Anchored.__init__(self)

    @property
    def current_node(self):
        if not self.current_node_id:
            return None
        elif not self._h.has_obj(uuid.UUID(self.current_node_id)):
            self.current_node_id = None
            return None
        else:
            return self._h.get_obj(self._m_id, uuid.UUID(self.current_node_id))

    @current_node.setter
    def current_node(self, obj):
        if obj:
            self.current_node_id = obj.id.urn
        else:
            self.current_node_id = None

    def namespace_keys(self):
        """Return list of md5 keys for namespaces"""
        ret = {}
        for i in self.namespaces:
            ret[i] = hashlib.md5((self._m_id + i).encode()).hexdigest()
        return ret

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
        self.run_walker(jac_ast=self.get_architype()._jac_ast)
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
        if not self.yielded:
            self.clear_state()
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
        if self._h.task.is_running() and self._async in Walker.valid_async:
            task_id = self._h.task.add_queue(
                self, start_node, prime_ctx, request_ctx, profiling
            )
            return {"task_id": task_id}

        if profiling:
            pr = cProfile.Profile()
            pr.enable()

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
        except Exception as e:
            import traceback as tb

            self.rt_error(f"Internal Exception: {e}", self._cur_jac_ast)
            report_ret["stack_trace"] = tb.format_exc()

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
        if len(self.runtime_errors):
            report_ret["errors"] = self.runtime_errors
            report_ret["success"] = False
        if profiling:
            pr.disable()
            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            s = s.getvalue()
            s = "ncalls" + s.split("ncalls")[-1]
            s = "\n".join(
                [",".join(line.rstrip().split(None, 5)) for line in s.split("\n")]
            )
            self.profile["perf"] = s
            report_ret["profile"] = self.profile

        return report_ret

    def yield_walk(self):
        """Instructs walker to yield (stop walking and keep state)"""
        self.yielded = True

    def log_history(self, name, value):
        """Helper function for logging history of walker's activities"""
        if isinstance(value, Element):
            value = {"type": value.j_type, "id": value.id.urn}
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
        self.activity_action_ids.destroy_all()
        self.context = {}
        WalkerInterp.reset(self)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        if not self._h.task.is_running() or self._async not in Walker.valid_async:
            for i in self.activity_action_ids.obj_list():
                i.destroy()
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
