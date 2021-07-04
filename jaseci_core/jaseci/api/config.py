"""
Admin config api functions as a mixin
"""


class config_api():
    """
    Admin config APIs
    """

    def admin_api_config_get(self, name: str):
        """
        Get a config
        """
        return self._h.get_cfg(name)

    def admin_api_config_set(self, name: str, value: str):
        """
        Set a config
        """
        self._h.save_cfg(name, value)
        return [f"Config of '{name}' to '{value}' set!"]

    def admin_api_config_list(self):
        """
        Check a config is present
        """
        return self._h.list_cfg()

    def admin_api_config_exists(self, name: str):
        """
        Check a config is present
        """
        return self._h.has_cfg(name)
