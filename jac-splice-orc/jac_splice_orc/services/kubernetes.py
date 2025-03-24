"""Kubenertes Services."""

from base64 import b64decode, b64encode
from datetime import UTC, datetime
from os import getenv, listdir, makedirs
from pathlib import Path
from re import compile
from shutil import rmtree
from subprocess import CompletedProcess, run
from typing import Any

from fastapi import HTTPException

from kubernetes import config
from kubernetes.client import ApiClient, AppsV1Api, CoreV1Api
from kubernetes.client.rest import ApiException

from orjson import dumps, loads

from ..dtos.deployment import Deployment, ModulesType
from ..utils import logger, utc_timestamp

PLACEHOLDERS_GENERIC = compile(r"(\$g\s*{\s*([^:\s]+)\s*(?:\:\s*([\S\s]*?))?\s*})")
PLACEHOLDERS_ARRAY = compile(
    r"((\ *(?:-\s)?)\s*\$a\s*{\s*([^:\s]+)\s*(?:\:\s*(\[[\S\s]*?\]))?\s*})"
)
PLACEHOLDERS_DICT = compile(
    r"((\ *)(?:-\s)?\$d\s*{\s*([^:\s]+)\s*(?:\:\s*(\{[\S\s]*?\}))?\s*})"
)


class KubernetesService:
    """Kubernetes Service."""

    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

    namespace = getenv("NAMESPACE", "default")
    cluster_wide = getenv("CLUSTER_WIDE") == "true"
    manifests = Path(getenv("MANIFESTS_PATH", "/tmp/manifests"))

    assert manifests.is_dir(), f"Not a valid path: {manifests}"

    app = ApiClient()
    core = CoreV1Api()
    api = AppsV1Api(app)

    assert app.call_api("/readyz", "GET")[1] == 200

    @classmethod
    def get_modules(cls) -> ModulesType:
        """Get modules."""
        try:
            return loads(
                b64decode(
                    cls.core.read_namespaced_secret(
                        name="jac-orc",
                        namespace=cls.namespace,
                    ).data["MODULES"]
                )
            )
        except Exception:
            logger.exception(f"Error getting modules with namespace: `{cls.namespace}`")
            return {}

    @classmethod
    def create_namespace_if_not_existing(cls, namespace: str) -> None:
        """Create namespace."""
        try:
            cls.core.create_namespace(
                {
                    "apiVersion": "v1",
                    "kind": "Namespace",
                    "metadata": {"name": namespace},
                },
            )
        except Exception as e:
            logger.error(f"Error creating namespace {namespace} skipping... {e}")

    @classmethod
    def get_module_paths(cls, deployment: Deployment) -> tuple[Path, Path]:
        """Get module paths."""
        if cls.cluster_wide or not deployment.config.get("namespace"):
            deployment.config["namespace"] = cls.namespace

        module_path = Path(f"{cls.manifests}/{deployment.module}")
        if not module_path.is_dir():
            raise HTTPException(
                400, f"Deployment for {deployment.module} is not yet supported!"
            )

        version_path = Path(f"{module_path}/{deployment.version}")
        if not version_path.is_dir():
            raise HTTPException(
                400,
                f"Deployment for {deployment.module} with version `{deployment.version}` is not yet supported!\n"
                f"Valid versions: {', '.join(p.name for p in module_path.iterdir())}",
            )

        return version_path, Path(f"{version_path}/dependencies")

    @classmethod
    def update_modules(cls, deployment: Deployment) -> None:
        """Update modules."""
        modules = cls.get_modules()

        namespace: str = deployment.config["namespace"]
        if not (target_namespace := modules.get(namespace)):
            target_namespace = modules[namespace] = {}

        module: str = deployment.module
        if not (target_module := target_namespace.get(module)):
            target_module = target_namespace[module] = {}

        target_module[deployment.config["name"]] = deployment.model_dump(mode="json")

        try:
            cls.core.patch_namespaced_secret(
                name="jac-orc",
                namespace=cls.namespace,
                body={"data": {"MODULES": b64encode(dumps(modules)).decode()}},
            )
        except Exception:
            logger.exception(
                f"Error updating modules with request: `{deployment.model_dump_json()}`"
            )

    @classmethod
    def apply_manifests(
        cls, path: Path, config: dict[str, Any]
    ) -> tuple[CompletedProcess[str], dict[str, Any]]:
        """Apply Manifests."""
        tmp = Path(f"{path}/tmp-{utc_timestamp()}")
        makedirs(tmp, exist_ok=True)

        parsed_config: dict[str, Any] = {}

        for manifest in listdir(path):
            if manifest.endswith(".yaml") or manifest.endswith(".yml"):
                with open(f"{path}/{manifest}", "r") as stream:
                    raw = stream.read()

                for placeholder in set(PLACEHOLDERS_GENERIC.findall(raw)):
                    prefix = placeholder[1]
                    default = loads((placeholder[2] or '""').encode())
                    current = config.get(prefix, default)
                    raw = raw.replace(placeholder[0], str(current))
                    parsed_config[prefix] = current

                for placeholder in set(PLACEHOLDERS_ARRAY.findall(raw)):
                    spaces = placeholder[1]
                    prefix = placeholder[2]
                    default = loads((placeholder[3] or "[]").encode())
                    current = ""
                    _current = config.get(prefix, default)
                    for arg in _current:
                        current += f"{spaces}{arg}\n"

                    raw = raw.replace(placeholder[0], current)
                    parsed_config[prefix] = _current

                for placeholder in set(PLACEHOLDERS_DICT.findall(raw)):
                    spaces = placeholder[1]
                    prefix = placeholder[2]
                    default = loads((placeholder[3] or "{}").encode())
                    current = ""
                    _current = config.get(prefix, default)
                    for key, value in _current.items():
                        current += f"{spaces}{key}: {value}\n"

                    raw = raw.replace(placeholder[0], current)
                    parsed_config[prefix] = _current

                with open(f"{tmp}/{manifest}", "w") as stream:
                    stream.write(raw)

        cls.create_namespace_if_not_existing(parsed_config["namespace"])

        output = run(
            ["kubectl", "apply", "-f", tmp],
            capture_output=True,
            text=True,
        )

        rmtree(tmp)

        return output, parsed_config

    @classmethod
    def view_manifests(
        cls, path: Path, config: dict[str, Any]
    ) -> tuple[dict[str, str], dict[str, dict[str, dict[str, Any]]]]:
        """View Manifests."""
        manifests: dict[str, str] = {}
        placeholders: dict[str, dict[str, dict[str, Any]]] = {}

        for manifest in listdir(path):
            if manifest.endswith(".yaml") or manifest.endswith(".yml"):
                with open(f"{path}/{manifest}", "r") as stream:
                    raw = stream.read()

                for placeholder in set(PLACEHOLDERS_GENERIC.findall(raw)):
                    prefix = placeholder[1]
                    default = loads((placeholder[2] or '""').encode())
                    current = config.get(prefix, default)
                    raw = raw.replace(placeholder[0], str(current))
                    placeholders[prefix] = {"current": current, "default": default}

                for placeholder in set(PLACEHOLDERS_ARRAY.findall(raw)):
                    spaces = placeholder[1]
                    prefix = placeholder[2]
                    default = loads((placeholder[3] or "[]").encode())
                    current = ""
                    _current = config.get(prefix, default)
                    for arg in _current:
                        current += f"{spaces}{arg}\n"

                    raw = raw.replace(placeholder[0], current)
                    placeholders[prefix] = {"current": _current, "default": default}

                for placeholder in set(PLACEHOLDERS_DICT.findall(raw)):
                    spaces = placeholder[1]
                    prefix = placeholder[2]
                    default = loads((placeholder[3] or "{}").encode())
                    current = ""
                    _current = config.get(prefix, default)
                    for key, value in _current.items():
                        current += f"{spaces}{key}: {value}\n"

                    raw = raw.replace(placeholder[0], current)
                    placeholders[prefix] = {"current": _current, "default": default}

                manifests[manifest] = raw
        return manifests, placeholders

    @classmethod
    def restart(cls) -> None:
        """Restart Service."""
        try:
            return cls.api.patch_namespaced_deployment(
                name="jaseci",
                namespace=cls.namespace,
                body={
                    "spec": {
                        "template": {
                            "metadata": {
                                "annotations": {
                                    "kubectl.kubernetes.io/restartedAt": datetime.now(
                                        UTC
                                    ).isoformat("T")
                                    + "Z"
                                }
                            }
                        }
                    }
                },
            )
        except ApiException as e:
            logger.error(f"Error triggering jaseci rollout restart -- {e}")
