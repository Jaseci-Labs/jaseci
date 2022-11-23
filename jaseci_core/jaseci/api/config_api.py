"""
Admin config api functions as a mixin
"""
import yaml
from base64 import b64decode
from time import time

from json import dumps, loads
from jaseci.api.interface import Interface
from jaseci.svc import CommonService


class ConfigApi:
    """
    Admin config APIs
    Abstracted since there are no valid configs in core atm, see jaseci_serv
    to see how used.
    """

    def __init__(self, *args, **kwargs):
        self._valid_configs = [
            "CONFIG_EXAMPLE",
            "ACTION_SETS",
            "REDIS_CONFIG",
            "TASK_CONFIG",
            "MAIL_CONFIG",
            "KUBE_CONFIG",
            "PROMON_CONFIG",
            "JSORC_CONFIG",
        ]

    @Interface.admin_api(cli_args=["name"])
    def config_get(self, name: str, do_check: bool = True):
        """
        Get a config
        """
        if do_check and not self.name_check(name):
            return self.name_error(name)
        return self._h.get_glob(name)

    @Interface.admin_api(cli_args=["name"])
    def config_set(self, name: str, value: str or dict, do_check: bool = True):
        """
        Set a config
        """
        if do_check and not self.name_check(name):
            return self.name_error(name)

        if not (value is None) and type(value) is dict:
            value = dumps(value)

        self._h.save_glob(name, value)
        return [f"Config of '{name}' to '{value}' set!"]

    @Interface.admin_api()
    def config_yaml(self, name: str, file: list):
        """
        Set a config from yaml
        """

        new_config = {}

        config_version = str(time())

        for conf in yaml.safe_load_all(b64decode(file[0]["base64"])):
            kind = conf["kind"]
            labels = conf.get("metadata").get("labels")
            if not labels.get("config_version"):
                labels["config_version"] = config_version

            if not new_config.get(kind):
                new_config[kind] = []
            new_config[kind].append(conf)

        old_config = self._h.get_glob(name)
        if old_config:
            old_config = loads(old_config)
            old_config.pop("__OLD_CONFIG__", None)
            for kind, confs in old_config.items():
                names = []
                for conf in confs:
                    names.append(conf["metadata"]["name"])
                old_config[kind] = names

            new_config["__OLD_CONFIG__"] = old_config

        self._h.save_glob(name, dumps(new_config))

        return new_config

    @Interface.admin_api()
    def config_refresh(self, name: str):
        """
        refresh service configs
        """

        hook = self._h

        to_start = not hook.meta.is_automated()

        service = getattr(hook, name, None)

        response = {"success": False}

        if isinstance(service, CommonService):
            service.reset(hook, to_start)
            response["success"] = True
        else:
            response[
                "message"
            ] = f"{name} is not a valid service. Can not refresh config."

        return response

    @Interface.admin_api()
    def config_list(self):
        """
        Check a config is present
        """
        return [v for v in self._h.list_glob() if v in self._valid_configs]

    @Interface.admin_api()
    def config_index(self):
        """
        List all valid configs
        """
        return self._valid_configs

    @Interface.admin_api(cli_args=["name"])
    def config_exists(self, name: str):
        """
        Check a config is present
        """
        return self._h.has_glob(name)

    @Interface.admin_api(cli_args=["name"])
    def config_delete(self, name: str, do_check: bool = True):
        """
        Delete a config
        """
        if do_check and not self.name_check(name):
            return self.name_error(name)
        self._h.destroy_glob(name)
        return [f"{name} Deleted."]

    def name_error(self, name):
        """Much used error output"""
        return [f"Config {name} not recognized, must be in {self._valid_configs}!"]

    def name_check(self, name):
        """Much used name check"""
        return name in self._valid_configs
