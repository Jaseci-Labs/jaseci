import requests
import configparser
import os


class AIServingAPI():
    def __init__(self, API):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + '/ai-serving.config.ini')
        self.url = config.get(API, 'url')
        self.header = {'content-type': 'application/json'}

    def get(self):
        response = requests.get(self.url, headers=self.header)
        return response.json()

    def post(self, data):
        response = requests.post(self.url, headers=self.header, json=data)
        return response.json()
