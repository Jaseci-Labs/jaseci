from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.socket_svc import SocketService
from jaseci.utils.utils import master_from_meta, logger


def get():
    return JsOrc.svc("socket").poke(SocketService)


@jaseci_action(act_group=["ws"])
def notify_client(target: str, data: dict):
    get().notify("client", target, data)


@jaseci_action(act_group=["ws"])
def notify_group(target: str, data: dict):
    get().notify("group", target, data)


@jaseci_action(act_group=["ws"])
def notify_all(data: dict, meta: dict = {}):
    ss = get()

    mast = master_from_meta(meta)
    if not mast.is_master(super_check=True, silent=False):
        logger.error("You don't have permission to notify all clients!")
        return

    ss.send(ss.app, {"type": f"notify_all", "data": data})
