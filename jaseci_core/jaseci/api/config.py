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
                 'HTTP_LOGGING_HOST',
                 'HTTP_LOGGING_PORT',
                 'HTTP_LOGGING_URL',
                 ]


class config_api():
    """
    Admin config APIs
    """

    def admin_api_config_get(self, name: str,
                             do_check: bool = True):
        """
        Get a config
        """
        if(do_check and not self.name_check(name)):
            return self.name_error(name)
        return self._h.get_glob(name)

    def admin_api_config_set(self, name: str, value: str,
                             do_check: bool = True):
        """
        Set a config
        """
        if(do_check and not self.name_check(name)):
            return self.name_error(name)
        self._h.save_glob(name, value)
        if(name.startswith('HTTP_LOGGING')):
            self.reconnect_http_logging()
        return [f"Config of '{name}' to '{value}' set!"]

    def admin_api_config_list(self):
        """
        Check a config is present
        """
        return [v for v in self._h.list_glob() if v in VALID_CONFIGS]

    def admin_api_config_exists(self, name: str):
        """
        Check a config is present
        """
        return self._h.has_glob(name)

    def admin_api_config_delete(self, name: str,
                                do_check: bool = True):
        """
        Delete a config
        """
        if(do_check and not self.name_check(name)):
            return self.name_error(name)
        self._h.destroy_glob(name)
        return [f"{name} Deleted."]

    def name_error(name):
        """Much used error output"""
        return [
            f"Config {name} not recognized, must be in {VALID_CONFIGS}!"]

    def name_check(name):
        """Much used name check"""
        return (name in VALID_CONFIGS)
