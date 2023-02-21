from jaseci import JsOrc
from jaseci.svc.kube_svc import KubeService
from requests import get, post
from datetime import datetime
from copy import copy
from base64 import b64encode


#################################################
#                  ELASTIC APP                  #
#################################################


@JsOrc.service(name="elastic", config="ELASTIC_CONFIG", manifest="ELASTIC_MANIFEST")
class ElasticService(JsOrc.CommonService):
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def __init__(self, config: dict, manifest: dict):
        if not config.get("auth"):
            sec = JsOrc.svc("kube", KubeService).get_secret(
                "jaseci-es-elastic-user", "elastic", "elastic-system"
            )
            config["auth"] = f'basic {b64encode(f"elastic:{sec}".encode()).decode()}'

        super().__init__(config, manifest)

    def run(self):
        self.app = Elastic(self.config)
        self.app.health("timeout=1s")


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

    def _get(self, url: str, json: dict = None):
        return get(
            f"{self.url}{url}", json=json, headers=self.headers, verify=False
        ).json()

    def _post(self, url: str, json: dict = None):
        return post(
            f"{self.url}{url}", json=json, headers=self.headers, verify=False
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
        return self.get(f"/_mapping?{query}", index, suffix)

    def mapping_activity(self, query: str = "", suffix: str = ""):
        return self.mapping(query, self.activity_index, suffix)

    def aliases(self, query: str = "pretty=true"):
        return self._get(f"/_aliases?{query}")

    def reindex(self, body: dict, query: str = "pretty"):
        return self._post(f"/_reindex?{query}", body)

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

        headers = interp.request_context["headers"]
        if headers.get("Authorization"):
            del headers["Authorization"]

        activity = {
            "datetime": datetime.utcnow().isoformat(),
            "activity_action": action or walker.name.replace("_", " ").title(),
            "activity_type": walker.name,
            "activity_point": node.name,
            "walker_id": walker.jid,
            "node_id": node.jid,
            "master_id": meta["m_id"],
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
        if self._get(f"/_cluster/health?{query}")["timed_out"]:
            raise Exception("Cannot connect on elastic service!")
