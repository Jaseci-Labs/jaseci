import threading
import queue
import logging.handlers
from jaseci.utils.utils import logger
from jaseci.actions.live_actions import jaseci_action
from jaseci import JsOrc
from jaseci.svc.elastic_svc import ElasticService, Elastic


def elastic():
    return JsOrc.svc("elastic", ElasticService).poke(Elastic)


has_queue_handler = any(
    isinstance(h, logging.handlers.QueueHandler) for h in logger.handlers
)
if not has_queue_handler:
    log_queue = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    def elastic_log_worker():
        while True:
            try:
                record = log_queue.get()
                if record is None:
                    break
                elastic_record = {
                    "@timestamp": logging.Formatter().formatTime(
                        record, "%Y-%m-%d %H:%M:%S"
                    ),
                    "message": record.getMessage(),
                    "level": record.levelname,
                }
                elastic().doc(log=elastic_record)
            except Exception:
                pass

    worker_thread = threading.Thread(target=elastic_log_worker, daemon=True)
    worker_thread.start()


@jaseci_action()
def _post(url: str, json: dict = {}):
    return elastic()._post(url, json)


@jaseci_action()
def _get(url: str, json: dict = None):
    return elastic()._get(url, json)


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
def refresh(index: str = "", suffix: str = ""):
    return elastic().refresh(index, suffix)


@jaseci_action()
def refresh_activity(suffix: str = ""):
    return elastic().refresh_activity(suffix)


@jaseci_action()
def aliases(query: str = "pretty=true"):
    return elastic().aliases(query)


@jaseci_action()
def reindex(body: dict, query: str = "pretty"):
    return elastic().reindex(body, query)
