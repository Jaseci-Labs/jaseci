"""
Admin config api functions as a mixin
"""
from json import dumps, loads
from jaseci.utils.utils import manipulate_data
from jaseci.extens.api.interface import Interface


class ConfigApi:
    """
    Admin config APIs
    """

    @Interface.admin_api(cli_args=["name"])
    def config_get(self, name: str):
        """
        Get a config
        """
        conf = self._h.get_conf(name)
        if isinstance(conf, (str, bytes, bytearray)):
            try:
                return loads(conf)
            except Exception:
                pass

        return conf

    @Interface.admin_api(cli_args=["name"])
    def config_set(self, name: str, value: str or dict or list or tuple):
        """
        Set a config
        """
        if not (value is None) and isinstance(value, (dict, list, tuple)):
            value = dumps(value)

        self._h.save_conf(name, value)
        return [f"Config '{name}' to '{value}' set!"]

    @Interface.admin_api(cli_args=["name"])
    def config_update(
        self,
        name: str,
        field_key: str or int or list or tuple,
        field_value: str
        or int
        or float
        or list
        or dict
        or bool
        or tuple
        or None,  # json serializable types
    ):
        """
        Update a key-value of a config
        """
        conf = self._h.get_conf(name)
        try:
            conf = manipulate_data(conf, field_key, field_value)
            self._h.save_conf(name, conf)
            return [
                f"Config '{name}' is updated with {field_key}:{field_value}. Current config value: {conf}"
            ]
        except Exception as e:
            return [
                f"Config {name} is not a dictionary or list. Uses config_set to set the value for this config."
            ]

    @Interface.admin_api()
    def config_list(self):
        """
        Check a config is present
        """
        return self._h.list_conf()

    @Interface.admin_api(cli_args=["name"])
    def config_exists(self, name: str):
        """
        Check a config is present
        """
        return self._h.has_conf(name)

    @Interface.admin_api(cli_args=["name"])
    def config_delete(self, name: str):
        """
        Delete a config
        """
        self._h.destroy_conf(name)
        return [f"{name} Deleted."]
