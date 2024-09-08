import os
from time import time
from jaseci.jsorc.jsorc_utils import load_default_yaml, get_service_map


class JsOrcSettings:
    ###############################################################################################################
    # ------------------------------------------------- DEFAULT ------------------------------------------------- #
    ###############################################################################################################

    DEFAULT_CONFIG = {"enabled": False, "quiet": False, "automated": False}

    DEFAULT_MANIFEST = {}

    UNSAFE_PARAPHRASE = "I know what I'm doing!"
    UNSAFE_KINDS = ["PersistentVolumeClaim"]

    SERVICE_MANIFEST_MAP = get_service_map("database", "redis", "elastic", "prome")

    ###############################################################################################################
    # -------------------------------------------------- JSORC -------------------------------------------------- #
    ###############################################################################################################

    JSORC_CONFIG = {
        "backoff_interval": 10,
        "pre_loaded_services": [],
    }

    ###############################################################################################################
    # -------------------------------------------------- KUBE --------------------------------------------------- #
    ###############################################################################################################

    KUBE_NAMESPACE = os.getenv("KUBE_NAMESPACE", f"jaseci-{int(time() * 100000)}")

    KUBE_CONFIG = {
        "enabled": bool(os.getenv("KUBE_NAMESPACE")),
        "quiet": False,
        "automated": False,
        "namespace": KUBE_NAMESPACE,
        "in_cluster": True,
        "config": None,
    }

    ###############################################################################################################
    # -------------------------------------------------- REDIS -------------------------------------------------- #
    ###############################################################################################################

    REDIS_CONFIG = {
        "enabled": True,
        "quiet": False,
        "automated": False,
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": os.getenv("REDIS_PORT", "6379"),
        "db": os.getenv("REDIS_DB", "1"),
    }

    REDIS_MANIFEST = load_default_yaml("redis")

    ###############################################################################################################
    # -------------------------------------------------- TASK --------------------------------------------------- #
    ###############################################################################################################

    DEFAULT_REDIS_URL = (
        f'redis://{os.getenv("REDIS_HOST", "localhost")}'
        f':{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "1")}'
    )

    TASK_CONFIG = {
        "enabled": True,
        "quiet": False,
        "automated": False,
        "broker_url": DEFAULT_REDIS_URL,
        "result_backend": DEFAULT_REDIS_URL,
        "broker_connection_retry_on_startup": True,
        "task_track_started": True,
        "worker_redirect_stdouts": False,
    }

    ###############################################################################################################
    # -------------------------------------------------- MAIL --------------------------------------------------- #
    ###############################################################################################################

    MAIL_CONFIG = {
        "enabled": False,
        "quiet": False,
        "automated": False,
        "version": 2,
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
    }

    ###############################################################################################################
    # ------------------------------------------------- STRIPE -------------------------------------------------- #
    ###############################################################################################################

    STRIPE_CONFIG = {
        "enabled": False,
        "api_key": None,
        "automated": False,
        "webhook_key": None,
        "fallback_walker": "stripe",
        "event_walker": {},
    }

    ###############################################################################################################
    # ----------------------------------------------- PROMETHEUS ------------------------------------------------ #
    ###############################################################################################################

    PROME_CONFIG = {
        "enabled": bool(os.getenv("PROME_HOST")),
        "quiet": False,
        "automated": True,
        "url": (
            f'http://{os.getenv("PROME_HOST", "localhost")}'
            f':{os.getenv("PROME_PORT", "9090")}'
        ),
    }

    PROME_MANIFEST = load_default_yaml("prometheus")

    ###############################################################################################################
    # ------------------------------------------------ ELASTIC -------------------------------------------------- #
    ###############################################################################################################

    ELASTIC_ILM_POLICY_NAME = "jaseci-logs-ilm-policy"

    ELASTIC_ILM_POLICY = {
        "policy": {
            "phases": {
                "hot": {"actions": {"rollover": {"max_size": "1gb", "max_age": "7d"}}},
                "delete": {"min_age": "14d", "actions": {"delete": {}}},
            }
        }
    }

    ELASTIC_INDEX_TEMPLATE_NAME = "jaseci-logs-index-template"

    ELASTIC_INDEX_TEMPLATE = {
        "index_patterns": ["core*", "app*"],
        "data_stream": {},
        "composed_of": ["data-streams-mappings"],
        "priority": 500,
        "template": {"settings": {"index.lifecycle.name": ELASTIC_ILM_POLICY_NAME}},
    }

    ELASTIC_CONFIG = {
        "enabled": bool(os.getenv("ELASTIC_HOST")),
        "quiet": False,
        "automated": True,
        "url": (
            f'https://{os.getenv("ELASTIC_HOST", "localhost")}'
            f':{os.getenv("ELASTIC_PORT", "9200")}'
        ),
        "auth": os.getenv("ELASTIC_AUTH"),
        "common_index": f"{KUBE_NAMESPACE}-common",
        "activity_index": f"{KUBE_NAMESPACE}-activity",
        "core_log_index": "core",
        "app_log_index": "app",
        "ilm_policy_name": ELASTIC_ILM_POLICY_NAME,
        "ilm_policy": ELASTIC_ILM_POLICY,
        "index_template_name": ELASTIC_INDEX_TEMPLATE_NAME,
        "index_template": ELASTIC_INDEX_TEMPLATE,
    }

    ELASTIC_MANIFEST = load_default_yaml("elastic")

    ###############################################################################################################
    # ------------------------------------------------- STORAGE ------------------------------------------------- #
    ###############################################################################################################

    STORE_CONFIG = {
        "enabled": False,
        "quiet": False,
        "default": None,
        "providers": {},
    }

    STORE_MANIFEST = {}

    ###############################################################################################################
    # ------------------------------------------------ DATABASE ------------------------------------------------- #
    ###############################################################################################################

    DB_REGEN_CONFIG = {
        "enabled": os.environ.get("JSORC_DB_REGEN") == "true",
        "host": os.environ.get("POSTGRES_HOST", "jaseci-db"),
        "db": os.environ.get("DBNAME", "postgres"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "port": os.getenv("POSTGRES_PORT", 5432),
    }

    DB_REGEN_MANIFEST = load_default_yaml("database")
