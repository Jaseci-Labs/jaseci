import re
from jaseci.jsorc.jsorc import JsOrc
from jaseci.jsorc.jsorc_settings import JsOrcSettings
from jaseci.extens.svc.kube_svc import KubeService
from jaseci.utils.utils import logger, app_logger
from requests import get, post, put
from datetime import datetime
from copy import copy
from base64 import b64encode
import multiprocessing
import logging.handlers

LOG_QUEUES = {}


def format_elastic_record(record):
    # Strip out color code from message before sending to elastic
    msg = record.getMessage()
    msg = re.sub(r"\033\[[0-9]*m", "", msg)
    ts = "%s.%03d" % (
        logging.Formatter().formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        record.msecs,
    )

    elastic_record = {
        "@timestamp": ts,
        "message": msg,
        "level": record.levelname,
    }
    extra_fields = record.__dict__.get("extra_fields", [])
    elastic_record.update(dict([(k, record.__dict__[k]) for k in extra_fields]))
    return elastic_record


#################################################
#                  ELASTIC APP                  #
#################################################


@JsOrc.service(name="elastic", config="ELASTIC_CONFIG", manifest="ELASTIC_MANIFEST")
class ElasticService(JsOrc.CommonService):
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self):
        kube = JsOrc.svc("kube", KubeService)
        if kube.is_running():
            elasticsearches = kube.resolve_manifest(
                self.manifest, *JsOrc.overrided_namespace("elastic", self.manifest_type)
            ).get("Elasticsearch", [])

            if elasticsearches:
                metadata: dict = elasticsearches["jaseci"]["metadata"]

                cert = kube.get_secret(
                    f'{metadata.get("name")}-es-http-certs-internal',
                    "ca.crt",
                    metadata.get("namespace"),
                )

                if cert:
                    with open("elastic-certificate.crt", "w") as cert_file:
                        cert_file.write(cert)
                    self.config["verifier"] = "elastic-certificate.crt"

                if not self.config.get("auth"):
                    auth = kube.get_secret(
                        f'{metadata.get("name")}-es-elastic-user',
                        "elastic",
                        metadata.get("namespace"),
                    )
                    self.config[
                        "auth"
                    ] = f'basic {b64encode(f"elastic:{auth}".encode()).decode()}'

        self.app = Elastic(self.config)
        self.app.health("timeout=1s")

    def post_run(self):
        under_test = self.config.get("under_test", False)
        if not under_test:
            self.configure_elastic()
        LOG_QUEUES["core"] = self.add_elastic_log_handler(
            logger, self.config.get("core_log_index") or "core", under_test
        )
        LOG_QUEUES["app"] = self.add_elastic_log_handler(
            app_logger, self.config.get("app_log_index") or "app", under_test
        )

    def configure_elastic(self):
        """
        Configure elastic logging with desired configuration
        - Data stream for core* and app* index pattern
        - Index template with the data-streams-mappings component mapping rules
            - @timestamp is converted to date field type
            - text fields are converted as keywords for search
        - An index lifecycle management (ILM) policy
            - hot index for 7 days or 5GB max size
            - delete indices older than 30 days
        """
        # Create the ILM policy
        self.app.create_ilm_policy(
            policy_name=self.config.get(
                "ilm_policy_name", JsOrcSettings.ELASTIC_ILM_POLICY_NAME
            ),
            policy_config=self.config.get(
                "ilm_policy", JsOrcSettings.ELASTIC_ILM_POLICY
            ),
            overwrite=False,
        )

        # Create index template and attach ILM policy
        self.app.create_index_template(
            template_name=self.config.get(
                "index_template_name", JsOrcSettings.ELASTIC_INDEX_TEMPLATE_NAME
            ),
            template_config=self.config.get(
                "index_template", JsOrcSettings.ELASTIC_INDEX_TEMPLATE
            ),
            overwrite=False,
        )

    def add_elastic_log_handler(self, logger_instance, index, under_test=False):
        has_queue_handler = any(
            isinstance(h, logging.handlers.QueueHandler)
            for h in logger_instance.handlers
        )
        if not has_queue_handler:
            log_queue = multiprocessing.Queue()
            queue_handler = logging.handlers.QueueHandler(log_queue)
            logger_instance.addHandler(queue_handler)

            def elastic_log_worker(elastic_index):
                while True:
                    try:
                        record = log_queue.get()
                        if record is None:
                            # This is temporary
                            # for debugging purposes
                            from datetime import datetime

                            self.app.doc(
                                {
                                    "@timestamp": datetime.now().strftime(
                                        "%Y-%m-%dT%H:%M:%S"
                                    ),
                                    "message": f"Stopping process for {elastic_index}",
                                    "level": "SYSTEM",
                                },
                                index=elastic_index,
                            )
                            # end of temporary code
                            break
                        elastic_record = format_elastic_record(record)
                        self.app.doc(log=elastic_record, index=elastic_index)
                    except Exception:
                        pass

            # if under test, don't spawn the log worker process. Tests will validate two things:
            # 1. logs are added to the log queue
            # 2. format_elastic_record process the log properly and create the record for elastic
            if not under_test:
                worker_proc = multiprocessing.Process(
                    target=elastic_log_worker, args=(index,)
                )
                worker_proc.start()

            return log_queue


class Elastic:
    def __init__(self, config: dict):
        if not config.get("url"):
            raise Exception("URL is required!")
        self.url = config["url"]

        if not config.get("common_index"):
            raise Exception("Common Index is required!")
        self.common_index = config["common_index"]

        if not config.get("activity_index"):
            raise Exception("Activity Index is required!")
        self.activity_index = config["activity_index"]

        self.headers = {"Content-Type": "application/json"}

        if config["auth"]:
            self.headers["Authorization"] = config["auth"]

        self.verifier = config.get("verifier")

    def _get(self, url: str, json: dict = None):
        return get(
            f"{self.url}{url}",
            json=json,
            headers=self.headers,
            verify=self.verifier,
        ).json()

    def _post(self, url: str, json: dict = None):
        return post(
            f"{self.url}{url}",
            json=json,
            headers=self.headers,
            verify=self.verifier,
        ).json()

    def post(self, url: str, body: dict, index: str = "", suffix: str = ""):
        return self._post(f"/{index or self.common_index}{suffix}{url}", body)

    def post_act(self, url: str, body: dict, suffix: str = ""):
        return self.post(url, body, self.activity_index, suffix)

    def get(self, url: str, body: dict, index: str = "", suffix: str = ""):
        return self._get(f"/{index or self.common_index}{suffix}{url}", body)

    def get_act(self, url: str, body: dict, suffix: str = ""):
        return self.get(url, body, self.activity_index, suffix)

    def doc(self, log: dict, query: str = "", index: str = "", suffix: str = ""):
        return self.post(f"/_doc?{query}", log, index, suffix)

    def doc_activity(self, log: dict, query: str = "", suffix: str = ""):
        return self.doc(log, query, self.activity_index, suffix)

    def search(self, body: dict, query: str = "", index: str = "", suffix: str = ""):
        return self.get(f"/_search?{query}", body, index, suffix)

    def search_activity(self, body: dict, query: str = "", suffix: str = ""):
        return self.search(body, query, self.activity_index, suffix)

    def mapping(self, query: str = "", index: str = "", suffix: str = ""):
        return self.get(f"/_mapping?{query}", None, index, suffix)

    def mapping_activity(self, query: str = "", suffix: str = ""):
        return self.mapping(query, self.activity_index, suffix)

    def refresh(self, index: str = "", suffix: str = ""):
        return self.get(f"/_refresh", None, index, suffix)

    def refresh_activity(self, suffix: str = ""):
        return self.refresh(self.activity_index, suffix)

    def aliases(self, query: str = "pretty=true"):
        return self._get(f"/_aliases?{query}")

    def reindex(self, body: dict, query: str = "pretty"):
        return self._post(f"/_reindex?{query}", body)

    def create_ilm_policy(
        self, policy_name: str, policy_config: dict, overwrite: bool = False
    ):
        if not overwrite:
            res = get(
                f"{self.url}/_ilm/policy/{policy_name}",
                headers=self.headers,
                verify=self.verifier,
            )
            if res.status_code == 200 and policy_name in res.json():
                # policy already exists
                return False
        res = put(
            f"{self.url}/_ilm/policy/{policy_name}",
            headers=self.headers,
            json=policy_config,
            verify=self.verifier,
        )
        if res.status_code == 200:
            return res.json()
        else:
            return False

    def create_index_template(
        self, template_name: str, template_config: dict, overwrite: bool = False
    ):
        if not overwrite:
            res = get(
                f"{self.url}/_index_template/{template_name}",
                headers=self.headers,
                verify=self.verifier,
            )
            if res.status_code == 200 and template_name in res.json():
                # policy already exists
                return False
        res = put(
            f"{self.url}/_index_template/{template_name}",
            headers=self.headers,
            json=template_config,
            verify=self.verifier,
        )
        if res.status_code == 200:
            return res.json()
        else:
            return False

    # standard methods
    def generate_from_meta(self, meta: dict, override: dict, action: str = None):
        scope = meta["scope"].local_scope
        interp = meta["interp"]

        node = interp.current_node
        walker = scope["visitor"]

        override_misc = override.get("misc")
        override["misc"] = {
            "report": copy(interp.report),
            "node": node.serialize(detailed=False),
        }

        if override_misc and isinstance(override_misc, dict):
            override["misc"].update(override_misc)

        master = meta["h"].get_obj(meta["m_id"], meta["m_id"]).master_self(True)

        headers = interp.request_context.get("headers", {})
        if headers.get("Authorization"):
            del headers["Authorization"]

        activity = {
            "datetime": datetime.utcnow().isoformat(),
            "activity_action": action or walker.name.replace("_", " ").title(),
            "activity_type": walker.name,
            "activity_point": node.name,
            "walker_id": walker.jid,
            "node_id": node.jid,
            "master_id": master["jid"],
            "user": master.get("__meta__") or {"email": master["name"]},
            "request_context": interp.request_context,
            "data": walker.context,
        }

        activity.update(override)

        return activity

    def generate_from_request(self, request):
        headers = dict(request.headers)
        if headers.get("Authorization"):
            del headers["Authorization"]

        data = request.data.dict() if type(request.data) is not dict else request.data
        password = data.get("password")
        if password:
            data["password"] = len(password) * "*"

        user = request.user

        return {
            "datetime": datetime.utcnow().isoformat(),
            "activity_action": "User Manage",
            "activity_type": "user_manage",
            "master_id": user.master.urn,
            "user": {"email": user.email},
            "request_context": {
                "method": request.method,
                "headers": headers,
                "query": request.GET.dict(),
                "body": data,
            },
            "data": data,
        }

    def health(self, query: str = ""):
        if self._get(f"/_cluster/health?{query}").get("timed_out", True):
            raise Exception("Cannot connect on elastic service!")
