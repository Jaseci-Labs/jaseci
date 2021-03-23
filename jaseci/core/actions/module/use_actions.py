from .ai_serving_api import AIServingAPI

USE_API = AIServingAPI('USE')
USE_ENCODER_API = AIServiceAPI('USE_ENCODER')


def enc_question(param_list):
    """
    Encode question
    Param 1 - either string, or list of strings
    """
    data = {
        'op': 'encode_question',
        'text': param_list[0]
    }
    return USE_API.post(data)['encoded']


def enc_answer(param_list):
    """
    Encode Answer
    Param 1 - either string, or list of strings
    Param 2 - optional context, either string/list matching param 1
    """
    data = {
            'op': 'encode_answer',
            'text': param_list[0]
    }
    if(len(param_list) > 1):
        data['context'] = param_list[1]

    return USE_API.post(data)['encoded']


def dist_score(param_list):
    """
    Measure delta between USE endcodings
    Param 1 - First encoding from text
    Param 2 - Second ecoding from text
    """
    data = {
            'op': 'dist_score',
            'encoding': [param_list[0], param_list[1]]
    }
    return USE_API.post(data)['score']


def qa_score(param_list):
    """Macro for dist_score"""
    return dist_score(param_list)


def get_embedding(param_list):
    """
    Get the USE embeddings of the input text. (non-qa USE)
    Param 1 - either string or list of strings

    Return - Embeddings
    """
    data = {
        'op': 'encode',
        'text': param_list[0]
    }
    return USE_ENCODER_API.post(data)['encoded']
