"""
Logger api as a mixin
"""
from jaseci.api.interface import interface
from jaseci.utils.utils import logger, app_logger
from jaseci.utils.utils import connect_logger_handler
from logging.handlers import HTTPHandler


class logger_api():
    """
    APIs for Jaseci Logging configuration
    """

    @interface.admin_api(cli_args=['host'])
    def logger_http_connect(self, host: str, port: int,
                            url: str, log: str = 'all'):
        """
        Connects internal logging to http(s) (log msgs sent via POSTs)
        Valid log params: {sys, app, all }
        """
        num = 0
        if(log == 'sys' or log == 'all'):
            connect_logger_handler(
                logger, HTTPHandler(host=f'{host}:{port}',
                                    url=url, method='POST'))
            num += 1
        if(log == 'app' or log == 'all'):
            connect_logger_handler(
                app_logger, HTTPHandler(host=f'{host}:{port}',
                                        url=url, method='POST'))
            num += 1
        return [f'{num} http handlers added!']

    @interface.admin_api()
    def logger_http_clear(self, log: str = 'all'):
        """
        Connects internal logging to http(s) (log msgs sent via POSTs)
        Valid log params: {sys, app, all }
        """
        num = 0
        if(log == 'sys' or log == 'all'):
            for i in logger.handlers:
                if(i.__class__.__name__ == 'HTTPHandler'):
                    logger.removeHandler(i)
                    num += 1
        if(log == 'app' or log == 'all'):
            for i in app_logger.handlers:
                if(i.__class__.__name__ == 'HTTPHandler'):
                    app_logger.removeHandler(i)
                    num += 1
        return [f'{num} http handlers removed!']

    @interface.admin_api()
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
        return {'core': core, 'app': app}
