import os
import sys

import jaseci_serv.hook.orm  # noqa
from jaseci.jsorc.jsorc import JsOrc, JsOrcSettings as jss


class JsOrcSettings(jss):
    ###############################################################################################################
    # -------------------------------------------------- JSORC -------------------------------------------------- #
    ###############################################################################################################

    JSORC_CONFIG = {
        "backoff_interval": 10,
        "pre_loaded_services": ["redis", "prome", "mail", "task", "elastic", "store"],
    }

    ###############################################################################################################
    # -------------------------------------------------- TASK --------------------------------------------------- #
    ###############################################################################################################

    TASK_CONFIG = {
        "enabled": True,
        "quiet": True,
        "automated": True,
        "broker_url": f'redis://{os.getenv("REDIS_HOST", "localhost")}:{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "1")}',
        "beat_scheduler": "django_celery_beat.schedulers:DatabaseScheduler",
        "result_backend": "django-db",
        "task_track_started": True,
        "broker_connection_retry_on_startup": True,
        "worker_redirect_stdouts": False,
    }

    if "test" in sys.argv or any(["pytest" in arg for arg in sys.argv]):
        TASK_CONFIG["task_always_eager"] = True
        TASK_CONFIG["task_store_eager_result"] = True
        TASK_CONFIG["beat_scheduler"] = "celery.beat:PersistentScheduler"

    ###############################################################################################################
    # -------------------------------------------------- REDIS -------------------------------------------------- #
    ###############################################################################################################

    REDIS_CONFIG = {
        "enabled": os.getenv("REDIS_ENABLED", "true") == "true",
        "quiet": True,
        "automated": True,
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": os.getenv("REDIS_PORT", "6379"),
        "db": os.getenv("REDIS_DB", "1"),
    }


JsOrc._settings = JsOrcSettings
