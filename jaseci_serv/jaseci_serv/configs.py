###################################################
#                    SERVICES                     #
###################################################

import os
import sys

from jaseci_serv.kubes import PROMON_KUBE, REDIS_KUBE


RUN_SVCS = "test" in sys.argv or "runserver" in sys.argv

REDIS_CONFIG = {
    "enabled": True,
    "quiet": False,
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", "6379"),
    "db": os.getenv("REDIS_DB", "1"),
}

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

MAIL_CONFIG = {
    "enabled": True,
    "quiet": False,
    "version": 1,
    "tls": True,
    "host": "",
    "port": 587,
    "sender": "",
    "user": "",
    "pass": "",
    "backend": "smtp",
    "templates": {
        "activation_subj": "Please activate your account!",
        "activation_body": "Thank you for creating an account!\n\n"
        "Activation Code: {{code}}\n"
        "Please click below to activate:\n{{link}}",
        "activation_html_body": "Thank you for creating an account!<br><br>"
        "Activation Code: {{code}}<br>"
        "Please click below to activate:<br>"
        "{{link}}",
        "resetpass_subj": "Password Reset for Jaseci Account",
        "resetpass_body": "Your Jaseci password reset token is: {{token}}",
        "resetpass_html_body": "Your Jaseci password reset" "token is: {{token}}",
    },
    "migrate": False,
}

KUBE_CONFIG = {"enabled": False, "quiet": False, "in_cluster": False, "config": None}

JSORC_CONFIG = {
    "enabled": False,
    "quiet": False,
    "interval": 10,
    "namespace": "default",
    "keep_alive": ["promon", "redis", "task", "mail"],
}

PROMON_CONFIG = {
    "enabled": True,
    "quiet": False,
    "url": f'http://{os.getenv("PROMON_HOST", "localhost")}:{os.getenv("PROMON_PORT", "9090")}',
}

if "test" in sys.argv or "test_coverage" in sys.argv:
    MAIL_CONFIG["backend"] = "locmem"
    TASK_CONFIG["task_always_eager"] = True
    TASK_CONFIG["task_store_eager_result"] = True
    TASK_CONFIG["beat_scheduler"] = "celery.beat:PersistentScheduler"

# ----------------------------------------------- #
