from .ai_serving_api import AIServingAPI

BART_API = AIServingAPI('BART')


def eval_assoc(param_list):
    """
    Evaluate the assoication score between a given text and
    a list of categories or statements.
    Param 1 - string, the text in question
    Param 2 - list of strings, the list of categories to associate Param 1 to
    """
    data = {
            'op': 'eval_assoc',
            'text': param_list[0],
            'cats': param_list[1]
    }
    return BART_API.post(data)['sorted_associations']
