"""
Admin config api functions as a mixin
"""

from typing import Optional
from json import dumps, loads
from jaseci.extens.api.interface import Interface


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
            "PROME_CONFIG",
            "ELASTIC_CONFIG",
            "STRIPE_CONFIG",
            "KUBE_CONFIG",
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

    @Interface.admin_api(cli_args=["name"])
    def config_update(
        self,
        name: str,
        field_key: str,
        field_value: str
        or int
        or float
        or list
        or dict
        or bool
        or tuple
        or None,  # json serializable types
        do_check: bool = True,
    ):
        """
        Update a key-value of a config
        """
        if do_check and not self.name_check(name):
            return self.name_error(name)

        conf = self._h.get_glob(name)
        try:
            conf = loads(conf)
        except Exception:
            return [
                f"Config {name} is not a dictionary. Uses config_set to set the value for this config."
            ]
        if field_key not in conf:
            return [f"Field {field_key} does not exist in config {name}"]

        conf[field_key] = field_value
        conf = dumps(conf)
        self._h.save_glob(name, conf)
        return [
            f"Config of '{name}' is updated with {field_key}:{field_value}. Current config value: {conf}"
        ]

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
