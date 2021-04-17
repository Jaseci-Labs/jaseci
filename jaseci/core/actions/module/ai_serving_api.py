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

    def is_alive(self):
        try:
            requests.post(self.url, headers=self.header, json={})
        except:
            return False
        return True


def check_model_live(model_str):
    """Simple check to see if model is connected and live"""
    return AIServingAPI(model_str).is_alive()
