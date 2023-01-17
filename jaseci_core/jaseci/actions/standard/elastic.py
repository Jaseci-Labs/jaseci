from jaseci.actions.live_actions import jaseci_action
from jaseci.svc import MetaService


def elastic():
    return MetaService().get_service("elastic").poke()


@jaseci_action()
def post(url: str, body: dict, index: str = "", suffix: str = ""):
    return elastic().post(url, body, index, suffix)


@jaseci_action()
def post_act(url: str, body: dict, suffix: str = ""):
    return elastic().post_act(url, body, suffix)


@jaseci_action()
def get(url: str, body: dict, index: str = "", suffix: str = ""):
    return elastic().get(url, body, index)


@jaseci_action()
def get_act(url: str, body: dict, suffix: str = ""):
    return elastic().get_act(url, body, suffix)


@jaseci_action()
def doc(log: dict, query: str = "", index: str = "", suffix: str = ""):
    return elastic().doc(log, query, index, suffix)


@jaseci_action()
def doc_activity(log: dict, query: str = "", suffix: str = ""):
    return elastic().doc_activity(log, query, suffix)


@jaseci_action()
def search(body: dict, query: str = "", index: str = "", suffix: str = ""):
    return elastic().search(body, query, index, suffix)


@jaseci_action()
def search_activity(body: dict, query: str = "", suffix: str = ""):
    return elastic().search_activity(body, query, suffix)


@jaseci_action()
def mapping(query: str = "", index: str = "", suffix: str = ""):
    return elastic().mapping(query, index, suffix)


@jaseci_action()
def mapping_activity(query: str = "", suffix: str = ""):
    return elastic().mapping_activity(query, suffix)


@jaseci_action()
def aliases(query: str = "pretty=true"):
    return elastic().aliases(query)


@jaseci_action()
def reindex(body: dict, query: str = "pretty"):
    return elastic().reindex(body, query)
