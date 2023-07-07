"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from jaseci.prim.element import Element
from jaseci.jsorc.live_actions import live_actions, live_actions_lock
from jaseci.jac.jac_set import JacSet
import inspect
import time

from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.actions.actions_manager import ActionManager
from jaseci.jac.ir.jac_code import JacCode
from jaseci.jac.interpreter.interp import Interp
from jaseci.jac.machine.jac_scope import JacScope
from jaseci.utils.utils import logger


class Ability(Element, JacCode, Interp):
    """
    Abilities class for Jaseci
    """

    def __init__(
        self, code_ir=None, preset_in_out=None, access_list=None, *args, **kwargs
    ):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        self.access_list = access_list
        Element.__init__(self, *args, **kwargs)
        JacCode.__init__(self, code_ir=code_ir)
        Interp.__init__(self)

    def run_ability(self, here, visitor):
        """
        Run ability
        """
        Interp.__init__(self)  # Reset before as result need to be absorbed after
        self.push_scope(
            JacScope(
                parent=self,
                name=f"a_run:{self.get_jac_ast().loc_str()}",
                has_obj=here,
                here=here,
                visitor=visitor,
            )
        )
        self.run_code_block(self.get_jac_ast())
        self.pop_scope()

    def run_action(self, param_list, scope, interp):
        """
        param_list should be passed as list of values to lib functions
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        action_name = self.name
        if not interp.check_builtin_action(action_name):
            interp.rt_error(f"Cannot execute {action_name} - Not Found")
            return None
        # before_lock = time.time()
        live_actions_lock.reader_acquire()
        # logger.info(f"run_action reader acquire in {time.time()-before_lock}")
        try:
            func = live_actions[action_name]
            logger.info(
                f"============================== run_action ==================="
            )
            logger.info(f"got func {func}")
            args = inspect.getfullargspec(func)
            logger.info(f"got getfullargspec {args}")
            logger.info(f"got param_list {param_list}")

            self.do_auto_conversions(args, param_list)
            args = args[0] + args[4]
            logger.info(f"got getfullargspec {args}")
            logger.info(f"got param_list {param_list}")
            logger.info("============================================================")
            hook = scope.parent._h
            action_manager = JsOrc.get("action_manager", ActionManager)
            action_manager.pre_action_call_hook()

            # logger.info("after preaction callhook")
            ts = time.time()
            if "meta" in args:
                logger.info("in meta call")
                result = func(
                    *param_list["args"],
                    **param_list["kwargs"],
                    meta={
                        "m_id": scope.parent._m_id,
                        "h": scope.parent._h,
                        "scope": scope,
                        "interp": interp,
                    },
                )
            else:
                try:
                    if func.__module__ == "js_remote_hook":
                        # logger.info(f"remote action called for {action_name}")
                        result = func(*param_list["args"], **param_list["kwargs"])
                    else:
                        result = func(
                            self.name, *param_list["args"], **param_list["kwargs"]
                        )
                except TypeError as e:
                    params = str(inspect.signature(func))
                    interp.rt_error(
                        f"Invalid arguments {param_list} to action call {self.name}! Valid paramters are {params}.",
                        interp._cur_jac_ast,
                    )
                    logger.info(f"failing 1 {e}")
                    raise
                except Exception as e:
                    # Checking for race condition between walker running abilities and JSORC unloading modules
                    # if func != live_actions[action_name]:
                    #     logger.info(
                    #         "Action function pointer changed during execution. Retrying..."
                    #     )
                    #     return self.run_action(param_list, scope, interp)

                    interp.rt_error(
                        f"Exception within action call {self.name}! {e}",
                        interp._cur_jac_ast,
                    )
                    logger.info("failing 2")
                    raise
        finally:
            live_actions_lock.reader_release()
        # logger.info(f"run_action reader release in {time.time()-before_lock}")
        t = time.time() - ts
        action_manager.post_action_call_hook(action_name, t)
        return result

    def do_auto_conversions(self, args, params):
        """
        Automatically make conversions for jac to internal, e.g., list to jac_set
        """
        for i in args.annotations.keys():
            if args.annotations[i] == JacSet:
                idx = args.args.index(i)
                if idx < len(params["args"]):
                    params["args"][idx] = JacSet(in_list=params["args"][idx])
                if i in params["kwargs"]:
                    params["kwargs"][i] = JacSet(in_list=params["kwargs"][i])
