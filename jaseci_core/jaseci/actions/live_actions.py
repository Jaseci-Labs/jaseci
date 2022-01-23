"""
General action base class with automation for hot loading
"""
from importlib.util import spec_from_file_location, module_from_spec
from jaseci.utils.utils import logger

live_actions = {}


def jaseci_action(act_group=None):
    """Decorator for Jaseci Action interface"""
    def decorator_func(func):
        return assimilate_action(func, act_group)
    return decorator_func


def assimilate_action(func, act_group=None):
    """Helper for jaseci_action decorator"""
    global live_actions
    act_group = [func.__module__.split(
        '.')[-1]] if act_group is None else act_group
    live_actions[f"{'.'.join(act_group+[func.__name__])}"] = func
    return func


def load_actions(file):
    """Load all jaseci actions from python file"""
    spec = spec_from_file_location(str(file).split("/")[-1][:-3], str(file))
    if(spec is None):
        logger.error(f"Cannot hot load from action file {file}")
        return False
    else:
        spec.loader.exec_module(module_from_spec(spec))
        return True


def load_standard():
    import jaseci.actions.standard.net  # noqa
    import jaseci.actions.standard.rand  # noqa
    import jaseci.actions.standard.request  # noqa
    import jaseci.actions.standard.std  # noqa
    import jaseci.actions.standard.vector  # noqa


load_standard()


def get_global_actions(hook):
    """
    Loads all global action hooks for use by Jac programs
    Attaches globals to mem_hook
    """
    from jaseci.attr.action import action
    import uuid
    global_action_list = []
    for i in live_actions.keys():
        if(i.startswith('std.') or i.startswith('net.') or
           i.startswith('rand.') or i.startswith('vector.') or
           i.startswith('request.')):
            global_action_list.append(
                action(
                    m_id=uuid.UUID(int=0).urn,
                    h=hook,
                    mode='public',
                    name=i,
                    value=i,
                    persist=False
                ).jid
            )
    return global_action_list
