import sys

broker_url = "redis://localhost:6379/1"
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
result_backend = "django-db"
broker_connection_retry_on_startup = True
task_track_started = True

if "test" in sys.argv or "test_coverage" in sys.argv:
    task_always_eager = True
    task_store_eager_result = True
    beat_scheduler = "celery.beat:PersistentScheduler"

QUIET = False
