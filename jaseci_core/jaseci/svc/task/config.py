import os
import sys

DEFAULT_MSG = "Skipping scheduled walker!"
DEFAULT_URL = (
    f'redis://{os.getenv("REDIS_HOST", "localhost")}'
    f':{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "1")}'
)

TASK_CONFIG = {
    "enabled": True,
    "quiet": True,
    "broker_url": DEFAULT_URL,
    "result_backend": DEFAULT_URL,
    "broker_connection_retry_on_startup": True,
    "task_track_started": True,
    "worker_redirect_stdouts": False,
}


if "python3 -m unittest" in sys.argv:
    TASK_CONFIG["task_always_eager"] = True
    TASK_CONFIG["task_store_eager_result"] = True
