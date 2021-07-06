"""
Admin config api functions as a mixin
"""

VALID_CONFIGS = ['EMAIL_BACKEND',
                 'EMAIL_USE_TLS',
                 'EMAIL_HOST',
                 'EMAIL_HOST_USER',
                 'EMAIL_HOST_PASSWORD',
                 'EMAIL_PORT',
                 'EMAIL_DEFAULT_FROM',
                 'LOGSTASH_HOST',
                 'LOGSTASH_PORT',
                 ]


class config_api():
    """
    Admin config APIs
    """

    def admin_api_config_get(self, name: str):
        """
        Get a config
        """
        return self._h.get_cfg(name)

    def admin_api_config_set(self, name: str, value: str,
                             do_check: bool = True):
        """
        Set a config
        """
        if(do_check and name not in VALID_CONFIGS):
            return [
                f"Config {name} not recognized, must be in {VALID_CONFIGS}!"]
        self._h.save_cfg(name, value)
        if(name.startswith('LOGSTASH')):
            self.reconnect_logger_logstash()
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

    def admin_api_config_delete(self, name: str):
        """
        Delete a config
        """
        return self._h.destroy_cfg(name)
