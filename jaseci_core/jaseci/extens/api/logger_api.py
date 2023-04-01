"""
Logger api as a mixin
"""
import re
from jaseci.extens.api.interface import Interface
from jaseci.utils.log_utils import parse_logs
from jaseci.utils.utils import logger, app_logger, logs
from jaseci.utils.utils import connect_logger_handler
from logging.handlers import HTTPHandler


class LoggerApi:
    """
    APIs for Jaseci Logging configuration
    """

    @Interface.admin_api(cli_args=["host"])
    def logger_http_connect(self, host: str, port: int, url: str, log: str = "all"):
        """
        Connects internal logging to http(s) (log msgs sent via POSTs)
        Valid log params: {sys, app, all }
        """
        num = 0
        if log == "sys" or log == "all":
            connect_logger_handler(
                logger, HTTPHandler(host=f"{host}:{port}", url=url, method="POST")
            )
            num += 1
        if log == "app" or log == "all":
            connect_logger_handler(
                app_logger, HTTPHandler(host=f"{host}:{port}", url=url, method="POST")
            )
            num += 1
        return [f"{num} http handlers added!"]

    @Interface.admin_api()
    def logger_http_clear(self, log: str = "all"):
        """
        Connects internal logging to http(s) (log msgs sent via POSTs)
        Valid log params: {sys, app, all }
        """
        num = 0
        if log == "sys" or log == "all":
            for i in logger.handlers:
                if i.__class__.__name__ == "HTTPHandler":
                    logger.removeHandler(i)
                    num += 1
        if log == "app" or log == "all":
            for i in app_logger.handlers:
                if i.__class__.__name__ == "HTTPHandler":
                    app_logger.removeHandler(i)
                    num += 1
        return [f"{num} http handlers removed!"]

    @Interface.admin_api()
    def logger_get(self, search: str = "", level: str = None):
        """Get logs across loggers"""
        result = []
        for log in logs.getvalue().splitlines():
            # skip logs produced by calling this endpoint
            if re.search("Incoming call to logger_get", log):
                continue

            if search:
                if re.search(search, log):
                    result.append(log)
                continue

            result.append(log)

        result = parse_logs(result)

        if level:
            result = list(filter(lambda item: level and item["level"] == level, result))

        return result

    @Interface.admin_api()
    def logger_list(self):
        """
        Check active loggers
        """
        core = []
        app = []
        for i in logger.handlers:
            core.append(str(type(i)))
        for i in app_logger.handlers:
            app.append(str(type(i)))
        return {"core": core, "app": app}
