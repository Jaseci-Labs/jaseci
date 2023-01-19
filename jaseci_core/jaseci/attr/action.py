"""
Action class for Jaseci

Each action has an id, name, timestamp and it's set of edges.
"""
from .item import Item
from jaseci.actions.live_actions import live_actions
from jaseci.jac.jac_set import JacSet
import inspect
import time

# ACTION_PACKAGE = 'jaseci.actions.'


class Action(Item):
    """
    Action class for Jaseci

    preset_in_out holds a set of parameters in the form of lists of context
    objects that are to be used from whereever those contexts are attached
    e.g., (nodes, edges, walkers, etc). This is used by Jac's runtime
    engine to support preset actions in nodes
    access_list is used by walker to decide what to trigger
    """

    def __init__(self, preset_in_out=None, access_list=None, **kwargs):
        self.preset_in_out = preset_in_out  # Not using _ids convention
        self.access_list = access_list
        Item.__init__(self, **kwargs)

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

    def trigger(self, param_list, scope, interp):
        """
        param_list should be passed as list of values to lib functions
        Also note that Jac stores preset_in_out as input/output list of hex
        ids since preset_in_out doesn't use _ids convention
        """
        if not interp.check_builtin_action(self.value):
            interp.rt_error(f"Cannot execute {self.value} - Not Found")
            return None
        func = live_actions[self.value]
        args = inspect.getfullargspec(func)
        self.do_auto_conversions(args, param_list)
        args = args[0] + args[4]
        hook = scope.parent._h
        hook.meta.app.pre_action_call_hook() if hook.meta.run_svcs else None
        ts = time.time()
        if "meta" in args:
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
                result = func(*param_list["args"], **param_list["kwargs"])
            except TypeError as e:
                params = str(inspect.signature(func))
                interp.rt_error(
                    f"Invalid arguments {param_list} to action call {self.name}! Valid paramters are {params}.",
                    interp._cur_jac_ast,
                )
                raise
            except Exception as e:
                interp.rt_error(
                    f"Execption within action call {self.name}! {e}",
                    interp._cur_jac_ast,
                )
                raise
        t = time.time() - ts
        hook.meta.app.post_action_call_hook(
            self.value, t
        ) if hook.meta.run_svcs else None
        return result
