"""Built in actions for Jaseci"""
from .ai_serving_api import AIServingAPI

T5_API = AIServingAPI('T5')


def summarize(param_list, meta):
    """
    Summarize input text using T5 transformer models
    Param 1 - string, the text to be summarized
    Param 2 (Optional) - [min length, max length]
    """
    data = {
        'op': 'summary',
        'text': param_list[0]
    }
    if len(param_list) > 1:
        data['min_length'] = param_list[1][0]
        data['max_length'] = param_list[1][1]
    return T5_API.post(data)['summary']
