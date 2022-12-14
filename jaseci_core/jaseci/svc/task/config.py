import os

DEFAULT_MSG = "Skipping scheduled walker!"
DEFAULT_URL = (
    f'redis://{os.getenv("REDIS_HOST", "localhost")}'
    f':{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "1")}'
)

# default true
TASK_ENABLED = os.getenv("TASK_ENABLED", "true") == "true"

TASK_CONFIG = {
    "enabled": TASK_ENABLED,
    "quiet": True,
    "broker_url": DEFAULT_URL,
    "result_backend": DEFAULT_URL,
    "broker_connection_retry_on_startup": True,
    "task_track_started": True,
    "worker_redirect_stdouts": False,
}
