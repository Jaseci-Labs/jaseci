import os
import sys

TASK_CONFIG = {
    "enabled": True,
    "quiet": False,
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
