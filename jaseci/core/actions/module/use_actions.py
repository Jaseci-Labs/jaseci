from jac_api.apps import JacApiConfig


def enc_question(param_list):
    """
    Encode question
    Param 1 - either string, or list of strings
    """
    return JacApiConfig.USE.question_encode(param_list[0])


def enc_answer(param_list):
    """
    Encode Answer
    Param 1 - either string, or list of strings
    Param 2 - optional context, either string/list matching param 1
    """
    if (len(param_list) > 1):
        return JacApiConfig.USE.answer_encode(param_list[0],
                                              context=param_list[1])
    else:
        return JacApiConfig.USE.answer_encode(param_list[0])


def dist_score(param_list):
    """
    Measure delta between USE endcodings
    Param 1 - First encoding from text
    Param 2 - Second ecoding from text
    """
    return JacApiConfig.USE.dist_score(param_list[0], param_list[1])


def qa_score(param_list):
    """Macro for dist_score"""
    return dist_score(param_list)
