from flask import Flask
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class FlaskError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class AIServiceBase():

    def __init__(self, name=None):
        if name is None:
            name = __name__
        self.app = Flask(name)

    def log(self, level='INFO', message=''):
        self.app.logger.log(level, message)

    def run(self, host='0.0.0.0', port='80'):
        self.app.run(host=host, port=port)
