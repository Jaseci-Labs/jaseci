import re
import os
from enum import Enum
from yaml import safe_load_all, YAMLError
from typing import TypeVar, Any, Union

from multiprocessing import Process, current_process

from jaseci.utils.utils import logger

#######################################################################################################
#                                               HELPERS                                               #
#######################################################################################################

T = TypeVar("T")


def convert_yaml_manifest(file):
    manifest = {}
    try:
        for conf in safe_load_all(file):
            kind = conf["kind"]
            if not manifest.get(kind):
                manifest[kind] = {}
            manifest[kind].update({conf["metadata"]["name"]: conf})
    except YAMLError as exc:
        manifest = {"error": f"{exc}"}

    return manifest


def load_default_yaml(file):
    manifest = {}
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/manifests/{file}.yaml", "r"
    ) as stream:
        manifest = convert_yaml_manifest(stream)

    return manifest


def get_service_map(*services):
    service_map = {}
    for service in services:
        namespace = os.getenv(f"{service.upper()}_NAMESPACE")
        if namespace:
            service_map[service] = namespace

    return service_map


#######################################################################################################
#                                              RESOLVER                                               #
#######################################################################################################

placeholder_full = re.compile(r"^\$j\{(.*?)\}$")
placeholder_partial = re.compile(r"\$j\{(.*?)\}")
placeholder_splitter = re.compile(r"\.?([^\.\[\"\]]+)(?:\[\"?([^\"\]]+)\"?\])?")
# original
# placeholder_splitter = re.compile(r"([^\.\[\"\]]+)(?:\[\"?([^\"\]]+)\"?\])?(?:\.([^\.\[\"\]]+))?")


def get_splitter(val: str):
    matches = placeholder_splitter.findall(val)
    _matches = []
    for match in matches:
        for m in match:
            if m:
                _matches.append(m)
    return _matches


def get_value(source: dict, keys: list):
    if keys:
        key = keys.pop(0)
        if key in source:
            if keys:
                if isinstance(source[key], dict):
                    return get_value(source[key], keys)
            else:
                return source[key]
    return None


def placeholder_resolver(manifest, data: dict or list):
    for k, d in list(data.items()) if isinstance(data, dict) else enumerate(data):
        if isinstance(k, str):
            pk = k
            matcher = placeholder_full.search(k)
            if matcher:
                keys = get_splitter(matcher.group(1))
                pk = get_value(manifest, keys)
            else:
                for matcher in placeholder_partial.findall(k):
                    keys = get_splitter(matcher)
                    pk = pk.replace("$j{" + matcher + "}", get_value(manifest, keys))
            if pk != k:
                d = data.pop(k)
                k = pk
                data[pk] = d

        if isinstance(d, (dict, list)):
            placeholder_resolver(manifest, d)
        elif isinstance(d, str):
            matcher = placeholder_full.search(d)
            if matcher:
                keys = get_splitter(matcher.group(1))
                data[k] = get_value(manifest, keys)
            else:
                for matcher in placeholder_partial.findall(d):
                    keys = get_splitter(matcher)
                    data[k] = data[k].replace(
                        "$j{" + matcher + "}", get_value(manifest, keys)
                    )


#######################################################################################################
#                                                ENUMS                                                #
#######################################################################################################


class State(Enum):
    RESTART = -2
    FAILED = -1
    NOT_STARTED = 0
    STARTED = 1
    RUNNING = 2

    def is_ready(self):
        return self == State.NOT_STARTED

    def is_running(self):
        return self == State.RUNNING

    def has_failed(self):
        return self == State.FAILED


class ManifestType(Enum):
    SOURCE = -1
    DEDICATED = 0
    MANUAL = 1


#######################################################################################################
#                                               COMMON                                                #
#######################################################################################################


class CommonService:
    ###################################################
    #                   PROPERTIES                    #
    ###################################################

    # ------------------- DAEMON -------------------- #

    _daemon = {}

    @property
    def daemon(self):
        return __class__._daemon

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(
        self,
        config: dict,
        manifest: dict,
        manifest_type: ManifestType = ManifestType.DEDICATED,
        source: dict = {},
    ):
        self.app = None
        self.error = None
        self.state = State.NOT_STARTED
        self.source = source

        # ------------------- CONFIG -------------------- #

        self.config = config
        self.enabled = config.pop("enabled", False)
        self.quiet = config.pop("quiet", False)
        self.automated = config.pop("automated", False)

        # ------------------ MANIFEST ------------------- #

        self.manifest = manifest
        self.manifest_type = manifest_type
        self.manifest_unsafe_paraphrase = manifest.pop("__UNSAFE_PARAPHRASE__", "")

        self.start()

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def start(self):
        try:
            if self.enabled and self.is_ready():
                self.state = State.STARTED
                self.run()
                self.state = State.RUNNING
                self.post_run()
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    f"Skipping {self.__class__.__name__} due to initialization "
                    f"failure!\n{e.__class__.__name__}: {e}"
                )
            self.failed(e)

        return self

    def run(self):
        raise Exception(f"Not properly configured! Please override run method!")

    def post_run(self):
        pass

    # ------------------- DAEMON -------------------- #

    def spawn_daemon(self, **targets):
        if current_process().name == "MainProcess":
            for name, target in targets.items():
                dae: Process = self.daemon.get(name)
                if not dae or not dae.is_alive():
                    process = Process(target=target, daemon=True)
                    process.start()
                    self.daemon[name] = process

    def terminate_daemon(self, *names):
        for name in names:
            dae: Process = self.daemon.pop(name, None)
            if not (dae is None) and dae.is_alive():
                logger.info(f"Terminating {name} ...")
                dae.terminate()

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def poke(self, cast: T = None, msg: str = None) -> Union[T, Any]:
        if self.is_running():
            return (
                self if cast and cast.__name__ == self.__class__.__name__ else self.app
            )
        raise Exception(
            msg or f"{self.__class__.__name__} is disabled or not yet configured!"
        )

    def is_ready(self):
        return self.state.is_ready() and self.app is None

    def is_running(self):
        return self.state.is_running() and not (self.app is None)

    def has_failed(self):
        return self.state.has_failed()

    def failed(self, error: Exception = None):
        self.app = None
        self.state = State.FAILED
        self.error = error

    @classmethod
    def proxy(cls):
        return cls({}, {})

    # ---------------- PROXY EVENTS ----------------- #

    def on_delete(self):
        pass

    # ------------------- EVENTS -------------------- #

    def __del__(self):
        self.on_delete()

    def __getstate__(self):
        return {}

    def __setstate__(self, ignored):
        # for build on pickle load
        self.state = State.FAILED
        del self
