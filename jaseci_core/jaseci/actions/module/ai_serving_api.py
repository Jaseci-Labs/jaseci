import requests
import configparser
import os

ai_config_file = './ai-serving.config.ini' if os.path.exists('./ai-serving.config.ini') \
    else os.path.dirname(__file__) + '/ai-serving.config.ini'


class AIServingAPI():
    def __init__(self, API):
        config = configparser.ConfigParser()
        config.read(ai_config_file)
        self.url = config.get(API, 'url')
        self.header = {'content-type': 'application/json'}

    def get(self):
        response = requests.get(self.url, headers=self.header)
        return response.json()

    def post(self, data):
        response = requests.post(self.url, headers=self.header, json=data)
        return response.json()

    def is_alive(self):
        try:
            requests.post(self.url, headers=self.header, json={})
        except requests.exceptions.ConnectionError:
            return False
        return True


def check_model_live(model_str):
    """Simple check to see if model is connected and live"""
    return AIServingAPI(model_str).is_alive()
