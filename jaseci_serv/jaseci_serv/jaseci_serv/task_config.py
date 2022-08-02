broker_url = "redis://localhost:6379/1"
result_backend = "django-db"
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
broker_connection_retry_on_startup = True
task_track_started = True

QUIET = False
